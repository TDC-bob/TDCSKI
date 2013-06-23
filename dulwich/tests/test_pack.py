# test_pack.py -- Tests for the handling of git packs.
# Copyright (C) 2007 James Westby <jw+debian@jameswestby.net>
# Copyright (C) 2008 Jelmer Vernooij <jelmer@samba.org>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; version 2
# of the License, or (at your option) any later version of the license.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
# MA  02110-1301, USA.

"""Tests for Dulwich packs."""


from io import BytesIO
import os
import shutil
import tempfile
import zlib
import hashlib

from dulwich.errors import (
    ChecksumMismatch,
    )
from dulwich.file import (
    GitFile,
    )
from dulwich.object_store import (
    MemoryObjectStore,
    )
from dulwich.objects import (
    Blob,
    Commit,
    Tree,
    Blob,
    Sha1Sum,
    )
from dulwich.pack import (
    OFS_DELTA,
    REF_DELTA,
    DELTA_TYPES,
    MemoryPackIndex,
    Pack,
    PackData,
    apply_delta,
    create_delta,
    deltify_pack_objects,
    load_pack_index,
    UnpackedObject,
    read_zlib_chunks,
    write_pack_header,
    write_pack_index_v1,
    write_pack_index_v2,
    SHA1Writer,
    write_pack_object,
    write_pack,
    unpack_object,
    compute_file_sha,
    PackStreamReader,
    DeltaChainIterator,
    )
from dulwich.tests import (
    TestCase,
    )
from .utils import (
    make_object,
    build_pack,
    )

pack1_sha = Sha1Sum('bc63ddad95e7321ee734ea11a7a62d314e0d7481')
a_sha = Sha1Sum('6f670c0fb53f9463760b7295fbb814e965fb20c8')
tree_sha = Sha1Sum('b2a2766a2879c209ab1176e7e778b81ae422eeaa')
commit_sha = Sha1Sum('f18faa16531ac570a3fdc8c7ca16682548dafd12')


class PackTests(TestCase):
    """Base class for testing packs"""

    def setUp(self):
        super(PackTests, self).setUp()
        self.tempdir = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.tempdir)

    datadir = os.path.abspath(os.path.join(os.path.dirname(__file__),
        'data/packs'))

    def get_pack_index(self, sha):
        """Returns a PackIndex from the datadir with the given sha"""
        return load_pack_index(os.path.join(self.datadir, 'pack-%s.idx' % sha))

    def get_pack_data(self, sha):
        """Returns a PackData object from the datadir with the given sha"""
        return PackData(os.path.join(self.datadir, 'pack-%s.pack' % sha))

    def get_pack(self, sha):
        return Pack(os.path.join(self.datadir, 'pack-%s' % sha))

    def assertSucceeds(self, func, *args, **kwargs):
        try:
            func(*args, **kwargs)
        except ChecksumMismatch as e:
            self.fail(e)


class PackIndexTests(PackTests):
    """Class that tests the index of packfiles"""

    def test_object_index(self):
        """Tests that the correct object offset is returned from the index."""
        p = self.get_pack_index(pack1_sha)
        self.assertRaises(KeyError, p.object_index, pack1_sha)
        self.assertEqual(p.object_index(a_sha), 178)
        self.assertEqual(p.object_index(tree_sha), 138)
        self.assertEqual(p.object_index(commit_sha), 12)

    def test_index_len(self):
        p = self.get_pack_index(pack1_sha)
        self.assertEqual(3, len(p))

    def test_get_stored_checksum(self):
        p = self.get_pack_index(pack1_sha)
        self.assertEqual(Sha1Sum('f2848e2ad16f329ae1c92e3b95e91888daa5bd01'),
                         p.get_stored_checksum())
        self.assertEqual(Sha1Sum('721980e866af9a5f93ad674144e1459b8ba3e7b7'),
                         p.get_pack_checksum())

    def test_index_check(self):
        p = self.get_pack_index(pack1_sha)
        self.assertSucceeds(p.check)

    def test_iterentries(self):
        p = self.get_pack_index(pack1_sha)
        entries = [(Sha1Sum(s), o, c) for s, o, c in p.iterentries()]
        self.assertEqual([
          (Sha1Sum('6f670c0fb53f9463760b7295fbb814e965fb20c8'), 178, None),
          (Sha1Sum('b2a2766a2879c209ab1176e7e778b81ae422eeaa'), 138, None),
          (Sha1Sum('f18faa16531ac570a3fdc8c7ca16682548dafd12'), 12, None)
          ], entries)

    def test_iter(self):
        p = self.get_pack_index(pack1_sha)
        self.assertEqual(set([tree_sha, commit_sha, a_sha]), set(p))


class TestPackDeltas(TestCase):

    test_string1 = b'The answer was flailing in the wind'
    test_string2 = b'The answer was falling down the pipe'
    test_string3 = b'zzzzz'

    test_string_empty = b''
    test_string_big = b'Z' * 8192

    def _test_roundtrip(self, base, target):
        self.assertEqual(target,
                          b''.join(apply_delta(base, create_delta(base, target))))

    def test_nochange(self):
        self._test_roundtrip(self.test_string1, self.test_string1)

    def test_change(self):
        self._test_roundtrip(self.test_string1, self.test_string2)

    def test_rewrite(self):
        self._test_roundtrip(self.test_string1, self.test_string3)

    def test_overflow(self):
        self._test_roundtrip(self.test_string_empty, self.test_string_big)


class TestPackData(PackTests):
    """Tests getting the data from the packfile."""

    def test_create_pack(self):
        with self.get_pack_data(pack1_sha) as p:
            pass

    def test_from_file(self):
        path = os.path.join(self.datadir, 'pack-%s.pack' % str(pack1_sha))
        with PackData.from_file(open(path, 'rb'), os.path.getsize(path)) as p:
            pass

    def test_pack_len(self):
        with self.get_pack_data(pack1_sha) as p:
            self.assertEqual(3, len(p))

    def test_index_check(self):
        with self.get_pack_data(pack1_sha) as p:
            self.assertSucceeds(p.check)

    def test_iterobjects(self):
        with self.get_pack_data(pack1_sha) as p:
            commit_data = (b'tree b2a2766a2879c209ab1176e7e778b81ae422eeaa\n'
                           b'author James Westby <jw+debian@jameswestby.net> '
                           b'1174945067 +0100\n'
                           b'committer James Westby <jw+debian@jameswestby.net> '
                           b'1174945067 +0100\n'
                           b'\n'
                           b'Test commit\n')
            blob_sha = Sha1Sum('6f670c0fb53f9463760b7295fbb814e965fb20c8')
            tree_data = b'100644 a\0' + bytes(blob_sha)
            actual = []
            for offset, type_num, chunks, crc32 in p.iterobjects():
                actual.append((offset, type_num, b''.join(chunks), crc32))
            self.assertEqual([
              (12, 1, commit_data, 3775879613),
              (138, 2, tree_data, 912998690),
              (178, 3, b'test 1\n', 1373561701)
              ], actual)

    def test_iterentries(self):
        with self.get_pack_data(pack1_sha) as p:
            entries = set((Sha1Sum(s), o, c) for s, o, c in p.iterentries())
            self.assertEqual(set([
              (Sha1Sum('6f670c0fb53f9463760b7295fbb814e965fb20c8'), 178, 1373561701),
              (Sha1Sum('b2a2766a2879c209ab1176e7e778b81ae422eeaa'), 138, 912998690),
              (Sha1Sum('f18faa16531ac570a3fdc8c7ca16682548dafd12'), 12, 3775879613),
              ]), entries)

    def test_create_index_v1(self):
        with self.get_pack_data(pack1_sha) as p:
            filename = os.path.join(self.tempdir, 'v1test.idx')
            p.create_index_v1(filename)
            idx1 = load_pack_index(filename)
            idx2 = self.get_pack_index(pack1_sha)
            self.assertEqual(idx1, idx2)

    def test_create_index_v2(self):
        with self.get_pack_data(pack1_sha) as p:
            filename = os.path.join(self.tempdir, 'v2test.idx')
            p.create_index_v2(filename)
            idx1 = load_pack_index(filename)
            idx2 = self.get_pack_index(pack1_sha)
            self.assertEqual(idx1, idx2)

    def test_compute_file_sha(self):
        with BytesIO(b'abcd1234wxyz') as f:
            self.assertEqual(hashlib.sha1(b'abcd1234wxyz').hexdigest(),
                             compute_file_sha(f).hexdigest())
            self.assertEqual(hashlib.sha1(b'abcd1234wxyz').hexdigest(),
                             compute_file_sha(f, buffer_size=5).hexdigest())
            self.assertEqual(hashlib.sha1(b'abcd1234').hexdigest(),
                             compute_file_sha(f, end_ofs=-4).hexdigest())
            self.assertEqual(hashlib.sha1(b'1234wxyz').hexdigest(),
                             compute_file_sha(f, start_ofs=4).hexdigest())
            self.assertEqual(
              hashlib.sha1(b'1234').hexdigest(),
              compute_file_sha(f, start_ofs=4, end_ofs=-4).hexdigest())


class TestPack(PackTests):

    def test_len(self):
        with self.get_pack(pack1_sha) as p:
            self.assertEqual(3, len(p))

    def test_contains(self):
        with self.get_pack(pack1_sha) as p:
            self.assertTrue(tree_sha in p)

    def test_get(self):
        with self.get_pack(pack1_sha) as p:
            self.assertEqual(type(p[tree_sha]), Tree)

    def test_iter(self):
        with self.get_pack(pack1_sha) as p:
            self.assertEqual(set([tree_sha, commit_sha, a_sha]), set(p))

    def test_iterobjects(self):
        with self.get_pack(pack1_sha) as p:
            expected = set([p[s] for s in [commit_sha, tree_sha, a_sha]])
            self.assertEqual(expected, set(list(p.iterobjects())))

    def test_pack_tuples(self):
        with self.get_pack(pack1_sha) as p:
            tuples = p.pack_tuples()
            expected = set([(p[s], None) for s in [commit_sha, tree_sha, a_sha]])
            self.assertEqual(expected, set(list(tuples)))
            self.assertEqual(expected, set(list(tuples)))
            self.assertEqual(3, len(tuples))

    def test_get_object_at(self):
        """Tests random access for non-delta objects"""
        with self.get_pack(pack1_sha) as p:
            obj = p[a_sha]
            self.assertEqual(obj.type_name, 'blob')
            self.assertEqual(Sha1Sum(obj.sha()), a_sha)
            obj = p[tree_sha]
            self.assertEqual(obj.type_name, 'tree')
            self.assertEqual(Sha1Sum(obj.sha()), tree_sha)
            obj = p[commit_sha]
            self.assertEqual(obj.type_name, 'commit')
            self.assertEqual(Sha1Sum(obj.sha()), commit_sha)

    def test_copy(self):
        with self.get_pack(pack1_sha) as origpack:
            self.assertSucceeds(origpack.index.check)
            basename = os.path.join(self.tempdir, 'Elch')
            write_pack(basename, origpack.pack_tuples())
            with Pack(basename) as newpack:
                self.assertEqual(origpack, newpack)
                self.assertSucceeds(newpack.index.check)
                self.assertEqual(origpack.name(), newpack.name())
                self.assertEqual(origpack.index.get_pack_checksum(),
                                  newpack.index.get_pack_checksum())

                wrong_version = origpack.index.version != newpack.index.version
                orig_checksum = origpack.index.get_stored_checksum()
                new_checksum = newpack.index.get_stored_checksum()
                self.assertTrue(wrong_version or orig_checksum == new_checksum)

    def test_commit_obj(self):
        with self.get_pack(pack1_sha) as p:
            commit = p[commit_sha]
            self.assertEqual('James Westby <jw+debian@jameswestby.net>',
                             commit.author)
            self.assertEqual([], commit.parents)

    def _copy_pack(self, origpack):
        basename = os.path.join(self.tempdir, 'somepack')
        write_pack(basename, origpack.pack_tuples())
        return Pack(basename)

    def test_keep_no_message(self):
        with self.get_pack(pack1_sha) as tp:
            with self._copy_pack(tp) as p:

                keepfile_name = p.keep()
                # file should exist
                self.assertTrue(os.path.exists(keepfile_name))

                with open(keepfile_name, 'rb') as f:
                    buf = f.read()
                    self.assertEqual(b'', buf)

    def test_keep_message(self):
        with self.get_pack(pack1_sha) as tp:
            with self._copy_pack(tp) as p:

                msg = b'some message'
                keepfile_name = p.keep(msg)

                # file should exist
                self.assertTrue(os.path.exists(keepfile_name))

                # and contain the right message, with a linefeed
                with open(keepfile_name, 'rb') as f:
                    buf = f.read()
                    self.assertEqual(msg + b'\n', buf)

    def test_name(self):
        with self.get_pack(pack1_sha) as p:
            self.assertEqual(pack1_sha, Sha1Sum(p.name()))

    def test_length_mismatch(self):
        with self.get_pack_data(pack1_sha) as data:
            index = self.get_pack_index(pack1_sha)
            with Pack.from_objects(data, index) as p:
                p.check_length_and_checksum()
                data._file.seek(12)

                with BytesIO() as bad_file:
                    write_pack_header(bad_file, 9999)
                    bad_file.write(data._file.read())
                    with BytesIO(bad_file.getvalue()) as badder_file:
                        with PackData('', file=badder_file) as bad_data:
                            with Pack.from_lazy_objects(lambda: bad_data, lambda: index) as bad_pack:
                                self.assertRaises(AssertionError, lambda: bad_pack.data)
                                self.assertRaises(AssertionError,
                                  lambda: bad_pack.check_length_and_checksum())

    def test_checksum_mismatch(self):
        with self.get_pack_data(pack1_sha) as data:
            index = self.get_pack_index(pack1_sha)
            with Pack.from_objects(data, index) as p:
                p.check_length_and_checksum()

                data._file.seek(0)
                with BytesIO(data._file.read()[:-20] + (b'\xff' * 20)) as bad_file:
                    with PackData('', file=bad_file) as bad_data:
                        with Pack.from_lazy_objects(lambda: bad_data, lambda: index) as bad_pack:
                            self.assertRaises(ChecksumMismatch, lambda: bad_pack.data)
                            self.assertRaises(ChecksumMismatch, lambda:
                                              bad_pack.check_length_and_checksum())

    def test_iterobjects(self):
        with self.get_pack(pack1_sha) as p:
            objs = dict((o.id, o) for o in p.iterobjects())
            self.assertEqual(3, len(objs))
            self.assertEqual(sorted(objs), sorted(p.index))
            self.assertTrue(isinstance(objs[a_sha], Blob))
            self.assertTrue(isinstance(objs[tree_sha], Tree))
            self.assertTrue(isinstance(objs[commit_sha], Commit))

class WritePackTests(TestCase):

    def test_write_pack_header(self):
        with BytesIO() as f:
            write_pack_header(f, 42)
            self.assertEqual(b'PACK\x00\x00\x00\x02\x00\x00\x00*',
                             f.getvalue())

    def test_write_pack_object(self):
        with BytesIO() as f:
            f.write(b'header')
            offset = f.tell()
            crc32 = write_pack_object(f, Blob.type_num, b'blob')
            self.assertEqual(crc32, zlib.crc32(f.getvalue()[6:]) & 0xffffffff)

            f.write(b'x')  # unpack_object needs extra trailing data.
            f.seek(offset)
            comp_len = len(f.getvalue()) - offset - 1
            unpacked, unused = unpack_object(f.read, compute_crc32=True)
            self.assertEqual(Blob.type_num, unpacked.pack_type_num)
            self.assertEqual(Blob.type_num, unpacked.obj_type_num)
            self.assertEqual([b'blob'], unpacked.decomp_chunks)
            self.assertEqual(crc32, unpacked.crc32)
            self.assertEqual(b'x', unused)

    def test_write_pack_object_sha(self):
        with BytesIO() as f:
            f.write(b'header')
            offset = f.tell()
            sha_a = hashlib.sha1(b'foo')
            sha_b = sha_a.copy()
            write_pack_object(f, Blob.type_num, b'blob', sha=sha_a)
            self.assertNotEqual(sha_a.digest(), sha_b.digest())
            sha_b.update(f.getvalue()[offset:])
            self.assertEqual(sha_a.digest(), sha_b.digest())


pack_checksum = Sha1Sum('721980e866af9a5f93ad674144e1459b8ba3e7b7')


class BaseTestPackIndexWriting(object):

    def assertSucceeds(self, func, *args, **kwargs):
        try:
            func(*args, **kwargs)
        except ChecksumMismatch as e:
            self.fail(e)

    def index(self, filename, entries, pack_checksum):
        raise NotImplementedError(self.index)

    def test_empty(self):
        idx = self.index('empty.idx', [], pack_checksum)
        self.assertEqual(idx.get_pack_checksum(), pack_checksum)
        self.assertEqual(0, len(idx))

    def test_single(self):
        entry_sha = Sha1Sum('6f670c0fb53f9463760b7295fbb814e965fb20c8')
        my_entries = [(entry_sha, 178, 42)]
        idx = self.index('single.idx', my_entries, pack_checksum)
        self.assertEqual(idx.get_pack_checksum(), pack_checksum)
        self.assertEqual(1, len(idx))
        actual_entries = list(idx.iterentries())
        self.assertEqual(len(my_entries), len(actual_entries))
        for mine, actual in zip(my_entries, actual_entries):
            my_sha, my_offset, my_crc = mine
            actual_sha, actual_offset, actual_crc = actual
            self.assertEqual(my_sha, actual_sha)
            self.assertEqual(my_offset, actual_offset)
            if self._has_crc32_checksum:
                self.assertEqual(my_crc, actual_crc)
            else:
                self.assertTrue(actual_crc is None)


class BaseTestFilePackIndexWriting(BaseTestPackIndexWriting):

    def setUp(self):
        self.tempdir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.tempdir)

    def index(self, filename, entries, pack_checksum):
        path = os.path.join(self.tempdir, filename)
        self.writeIndex(path, entries, pack_checksum)
        idx = load_pack_index(path)
        self.assertSucceeds(idx.check)
        self.assertEqual(idx.version, self._expected_version)
        return idx

    def writeIndex(self, filename, entries, pack_checksum):
        # FIXME: Write to BytesIO instead rather than hitting disk ?
        f = GitFile(filename, "wb")
        try:
            self._write_fn(f, entries, pack_checksum)
        finally:
            f.close()


class TestMemoryIndexWriting(TestCase, BaseTestPackIndexWriting):

    def setUp(self):
        TestCase.setUp(self)
        self._has_crc32_checksum = True

    def index(self, filename, entries, pack_checksum):
        return MemoryPackIndex(entries, pack_checksum)

    def tearDown(self):
        TestCase.tearDown(self)


class TestPackIndexWritingv1(TestCase, BaseTestFilePackIndexWriting):

    def setUp(self):
        TestCase.setUp(self)
        BaseTestFilePackIndexWriting.setUp(self)
        self._has_crc32_checksum = False
        self._expected_version = 1
        self._write_fn = write_pack_index_v1

    def tearDown(self):
        TestCase.tearDown(self)
        BaseTestFilePackIndexWriting.tearDown(self)


class TestPackIndexWritingv2(TestCase, BaseTestFilePackIndexWriting):

    def setUp(self):
        TestCase.setUp(self)
        BaseTestFilePackIndexWriting.setUp(self)
        self._has_crc32_checksum = True
        self._expected_version = 2
        self._write_fn = write_pack_index_v2

    def tearDown(self):
        TestCase.tearDown(self)
        BaseTestFilePackIndexWriting.tearDown(self)


class ReadZlibTests(TestCase):

    decomp = (
      b'tree 4ada885c9196b6b6fa08744b5862bf92896fc002\n'
      b'parent None\n'
      b'author Jelmer Vernooij <jelmer@samba.org> 1228980214 +0000\n'
      b'committer Jelmer Vernooij <jelmer@samba.org> 1228980214 +0000\n'
      b'\n'
      b"Provide replacement for mmap()'s offset argument.")
    comp = zlib.compress(decomp)
    extra = b'nextobject'

    def setUp(self):
        super(ReadZlibTests, self).setUp()
        self.read = BytesIO(self.comp + self.extra).read
        self.unpacked = UnpackedObject(Tree.type_num, None, len(self.decomp), 0)

    def test_decompress_size(self):
        good_decomp_len = len(self.decomp)
        self.unpacked.decomp_len = -1
        self.assertRaises(ValueError, read_zlib_chunks, self.read,
                          self.unpacked)
        self.unpacked.decomp_len = good_decomp_len - 1
        self.assertRaises(zlib.error, read_zlib_chunks, self.read,
                          self.unpacked)
        self.unpacked.decomp_len = good_decomp_len + 1
        self.assertRaises(zlib.error, read_zlib_chunks, self.read,
                          self.unpacked)

    def test_decompress_truncated(self):
        read = BytesIO(self.comp[:10]).read
        self.assertRaises(zlib.error, read_zlib_chunks, read, self.unpacked)

        read = BytesIO(self.comp).read
        self.assertRaises(zlib.error, read_zlib_chunks, read, self.unpacked)

    def test_decompress_empty(self):
        unpacked = UnpackedObject(Tree.type_num, None, 0, None)
        comp = zlib.compress(b'')
        read = BytesIO(comp + self.extra).read
        unused = read_zlib_chunks(read, unpacked)
        self.assertEqual(b'', b''.join(unpacked.decomp_chunks))
        self.assertNotEqual(b'', unused)
        self.assertEqual(self.extra, unused + read())

    def test_decompress_no_crc32(self):
        self.unpacked.crc32 = None
        read_zlib_chunks(self.read, self.unpacked)
        self.assertEqual(None, self.unpacked.crc32)

    def _do_decompress_test(self, buffer_size, **kwargs):
        unused = read_zlib_chunks(self.read, self.unpacked,
                                  buffer_size=buffer_size, **kwargs)
        self.assertEqual(self.decomp, b''.join(self.unpacked.decomp_chunks))
        self.assertEqual(zlib.crc32(self.comp), self.unpacked.crc32)
        self.assertNotEqual(b'', unused)
        self.assertEqual(self.extra, unused + self.read())

    def test_simple_decompress(self):
        self._do_decompress_test(4096)
        self.assertEqual(None, self.unpacked.comp_chunks)

    # These buffer sizes are not intended to be realistic, but rather simulate
    # larger buffer sizes that may end at various places.
    def test_decompress_buffer_size_1(self):
        self._do_decompress_test(1)

    def test_decompress_buffer_size_2(self):
        self._do_decompress_test(2)

    def test_decompress_buffer_size_3(self):
        self._do_decompress_test(3)

    def test_decompress_buffer_size_4(self):
        self._do_decompress_test(4)

    def test_decompress_include_comp(self):
        self._do_decompress_test(4096, include_comp=True)
        self.assertEqual(self.comp, b''.join(self.unpacked.comp_chunks))


class DeltifyTests(TestCase):

    def test_empty(self):
        self.assertEqual([], list(deltify_pack_objects([])))

    def test_single(self):
        b = Blob.from_string(b"foo")
        self.assertEqual(
            [(b.type_num, b.sha().digest(), None, b.as_raw_string())],
            list(deltify_pack_objects([(b, b"")])))

    def test_simple_delta(self):
        b1 = Blob.from_string(b'a' * 101)
        b2 = Blob.from_string(b'a' * 100)
        delta = create_delta(b1.as_raw_string(), b2.as_raw_string())
        self.assertEqual([
            (b1.type_num, b1.sha().digest(), None, b1.as_raw_string()),
            (b2.type_num, b2.sha().digest(), b1.sha().digest(), delta)
            ],
            list(deltify_pack_objects([(b1, b""), (b2, b"")])))


class TestPackStreamReader(TestCase):

    def test_read_objects_emtpy(self):
        f = BytesIO()
        build_pack(f, [])
        reader = PackStreamReader(f.read)
        self.assertEqual(0, len(list(reader.read_objects())))

    def test_read_objects(self):
        f = BytesIO()
        entries = build_pack(f, [
          (Blob.type_num, b'blob'),
          (OFS_DELTA, (0, b'blob1')),
          ])
        reader = PackStreamReader(f.read)
        objects = list(reader.read_objects(compute_crc32=True))
        self.assertEqual(2, len(objects))

        unpacked_blob, unpacked_delta = objects

        self.assertEqual(entries[0][0], unpacked_blob.offset)
        self.assertEqual(Blob.type_num, unpacked_blob.pack_type_num)
        self.assertEqual(Blob.type_num, unpacked_blob.obj_type_num)
        self.assertEqual(None, unpacked_blob.delta_base)
        self.assertEqual(b'blob', b''.join(unpacked_blob.decomp_chunks))
        self.assertEqual(entries[0][4], unpacked_blob.crc32)

        self.assertEqual(entries[1][0], unpacked_delta.offset)
        self.assertEqual(OFS_DELTA, unpacked_delta.pack_type_num)
        self.assertEqual(None, unpacked_delta.obj_type_num)
        self.assertEqual(unpacked_delta.offset - unpacked_blob.offset,
                         unpacked_delta.delta_base)
        delta = create_delta(b'blob', b'blob1')
        self.assertEqual(delta, b''.join(unpacked_delta.decomp_chunks))
        self.assertEqual(entries[1][4], unpacked_delta.crc32)

    def test_read_objects_buffered(self):
        f = BytesIO()
        build_pack(f, [
          (Blob.type_num, b'blob'),
          (OFS_DELTA, (0, b'blob1')),
          ])
        reader = PackStreamReader(f.read, zlib_bufsize=4)
        self.assertEqual(2, len(list(reader.read_objects())))

    def test_read_objects_empty(self):
        reader = PackStreamReader(BytesIO().read)
        self.assertEqual([], list(reader.read_objects()))


class TestPackIterator(DeltaChainIterator):

    _compute_crc32 = True

    def __init__(self, *args, **kwargs):
        super(TestPackIterator, self).__init__(*args, **kwargs)
        self._unpacked_offsets = set()

    def _result(self, unpacked):
        """Return entries in the same format as build_pack."""
        return (unpacked.offset, unpacked.obj_type_num,
                b''.join(unpacked.obj_chunks), unpacked.sha(), unpacked.crc32)

    def _resolve_object(self, offset, pack_type_num, base_chunks):
        assert offset not in self._unpacked_offsets, (
                'Attempted to re-inflate offset %i' % offset)
        self._unpacked_offsets.add(offset)
        return super(TestPackIterator, self)._resolve_object(
          offset, pack_type_num, base_chunks)


class DeltaChainIteratorTests(TestCase):

    def setUp(self):
        super(DeltaChainIteratorTests, self).setUp()
        self.store = MemoryObjectStore()
        self.fetched = set()

    def store_blobs(self, blobs_data):
        blobs = []
        for data in blobs_data:
            blob = make_object(Blob, data=data)
            blobs.append(blob)
            self.store.add_object(blob)
        return blobs

    def get_raw_no_repeat(self, sha):
        """Wrapper around store.get_raw that doesn't allow repeat lookups."""
        self.assertFalse(sha in self.fetched,
                         'Attempted to re-fetch object %s' % sha)
        self.fetched.add(sha)
        return self.store.get_raw(sha)

    def make_pack_iter(self, f, thin=None):
        if thin is None:
            thin = bool(list(self.store))
        resolve_ext_ref = thin and self.get_raw_no_repeat or None
        data = PackData('test.pack', file=f)
        return TestPackIterator.for_pack_data(
          data, resolve_ext_ref=resolve_ext_ref)

    def assertEntriesMatch(self, expected_indexes, entries, pack_iter):
        expected = [entries[i] for i in expected_indexes]
        self.assertEqual(expected, list(pack_iter._walk_all_chains()))

    def test_no_deltas(self):
        f = BytesIO()
        entries = build_pack(f, [
          (Commit.type_num, b'commit'),
          (Blob.type_num, b'blob'),
          (Tree.type_num, b'tree'),
          ])
        self.assertEntriesMatch([0, 1, 2], entries, self.make_pack_iter(f))

    def test_ofs_deltas(self):
        f = BytesIO()
        entries = build_pack(f, [
          (Blob.type_num, b'blob'),
          (OFS_DELTA, (0, b'blob1')),
          (OFS_DELTA, (0, b'blob2')),
          ])
        self.assertEntriesMatch([0, 1, 2], entries, self.make_pack_iter(f))

    def test_ofs_deltas_chain(self):
        f = BytesIO()
        entries = build_pack(f, [
          (Blob.type_num, b'blob'),
          (OFS_DELTA, (0, b'blob1')),
          (OFS_DELTA, (1, b'blob2')),
          ])
        self.assertEntriesMatch([0, 1, 2], entries, self.make_pack_iter(f))

    def test_ref_deltas(self):
        f = BytesIO()
        entries = build_pack(f, [
          (REF_DELTA, (1, b'blob1')),
          (Blob.type_num, (b'blob')),
          (REF_DELTA, (1, b'blob2')),
          ])
        self.assertEntriesMatch([1, 0, 2], entries, self.make_pack_iter(f))

    def test_ref_deltas_chain(self):
        f = BytesIO()
        entries = build_pack(f, [
          (REF_DELTA, (2, b'blob1')),
          (Blob.type_num, (b'blob')),
          (REF_DELTA, (1, b'blob2')),
          ])
        self.assertEntriesMatch([1, 2, 0], entries, self.make_pack_iter(f))

    def test_ofs_and_ref_deltas(self):
        # Deltas pending on this offset are popped before deltas depending on
        # this ref.
        f = BytesIO()
        entries = build_pack(f, [
          (REF_DELTA, (1, b'blob1')),
          (Blob.type_num, (b'blob')),
          (OFS_DELTA, (1, b'blob2')),
          ])
        self.assertEntriesMatch([1, 2, 0], entries, self.make_pack_iter(f))

    def test_mixed_chain(self):
        f = BytesIO()
        entries = build_pack(f, [
          (Blob.type_num, b'blob'),
          (REF_DELTA, (2, b'blob2')),
          (OFS_DELTA, (0, b'blob1')),
          (OFS_DELTA, (1, b'blob3')),
          (OFS_DELTA, (0, b'bob')),
          ])
        self.assertEntriesMatch([0, 2, 1, 3, 4], entries,
                                self.make_pack_iter(f))

    def test_long_chain(self):
        n = 100
        objects_spec = [(Blob.type_num, b'blob')]
        for i in range(n):
            objects_spec.append((OFS_DELTA, (i, ('blob%i' % i).encode('utf-8'))))
        f = BytesIO()
        entries = build_pack(f, objects_spec)
        self.assertEntriesMatch(range(n + 1), entries, self.make_pack_iter(f))

    def test_branchy_chain(self):
        n = 100
        objects_spec = [(Blob.type_num, b'blob')]
        for i in range(n):
            objects_spec.append((OFS_DELTA, (0, ('blob%i' % i).encode('utf-8'))))
        f = BytesIO()
        entries = build_pack(f, objects_spec)
        self.assertEntriesMatch(range(n + 1), entries, self.make_pack_iter(f))

    def test_ext_ref(self):
        blob, = self.store_blobs([b'blob'])
        f = BytesIO()
        entries = build_pack(f, [(REF_DELTA, (blob.id, b'blob1'))],
                             store=self.store)
        pack_iter = self.make_pack_iter(f)
        self.assertEntriesMatch([0], entries, pack_iter)
        self.assertEqual([Sha1Sum(blob.id)], pack_iter.ext_refs())

    def test_ext_ref_chain(self):
        blob, = self.store_blobs([b'blob'])
        f = BytesIO()
        entries = build_pack(f, [
          (REF_DELTA, (1, b'blob2')),
          (REF_DELTA, (blob.id, b'blob1')),
          ], store=self.store)
        pack_iter = self.make_pack_iter(f)
        self.assertEntriesMatch([1, 0], entries, pack_iter)
        self.assertEqual([Sha1Sum(blob.id)], pack_iter.ext_refs())

    def test_ext_ref_multiple_times(self):
        blob, = self.store_blobs([b'blob'])
        f = BytesIO()
        entries = build_pack(f, [
          (REF_DELTA, (blob.id, b'blob1')),
          (REF_DELTA, (blob.id, b'blob2')),
          ], store=self.store)
        pack_iter = self.make_pack_iter(f)
        self.assertEntriesMatch([0, 1], entries, pack_iter)
        self.assertEqual([Sha1Sum(blob.id)], pack_iter.ext_refs())

    def test_multiple_ext_refs(self):
        b1, b2 = self.store_blobs([b'foo', b'bar'])
        f = BytesIO()
        entries = build_pack(f, [
          (REF_DELTA, (b1.id, b'foo1')),
          (REF_DELTA, (b2.id, b'bar2')),
          ], store=self.store)
        pack_iter = self.make_pack_iter(f)
        self.assertEntriesMatch([0, 1], entries, pack_iter)
        self.assertEqual([Sha1Sum(b1.id), Sha1Sum(b2.id)],
                         pack_iter.ext_refs())

    def test_bad_ext_ref_non_thin_pack(self):
        blob, = self.store_blobs([b'blob'])
        f = BytesIO()
        entries = build_pack(f, [(REF_DELTA, (blob.id, b'blob1'))],
                             store=self.store)
        pack_iter = self.make_pack_iter(f, thin=False)
        try:
            list(pack_iter._walk_all_chains())
            self.fail()
        except KeyError as e:
            self.assertEqual(([blob.id],), e.args)

    def test_bad_ext_ref_thin_pack(self):
        b1, b2, b3 = self.store_blobs([b'foo', b'bar', b'baz'])
        f = BytesIO()
        entries = build_pack(f, [
          (REF_DELTA, (1, b'foo99')),
          (REF_DELTA, (b1.id, b'foo1')),
          (REF_DELTA, (b2.id, b'bar2')),
          (REF_DELTA, (b3.id, b'baz3')),
          ], store=self.store)
        del self.store[b2.id]
        del self.store[b3.id]
        pack_iter = self.make_pack_iter(f)
        try:
            list(pack_iter._walk_all_chains())
            self.fail()
        except KeyError as e:
            self.assertEqual((sorted([b2.id, b3.id]),), e.args)