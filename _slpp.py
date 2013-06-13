# -*- coding: UTF-8 -*-
#-------------------------------------------------------------------------------
# Author:      Bob Daribouca
#
# Copyright:   (c) Bob Daribouca 2013
# Licence:     CC BY-NC-SA 3.0
#
#               Please refer to the "LICENSE" file distributed with the package,
#               or to http://creativecommons.org/licenses/by-nc-sa/3.0/
#
#-------------------------------------------------------------------------------
#!/usr/bin/env python
import re
import Exceptions
from _logging._logging import logged, mkLogger, INFO
from collections import OrderedDict

logger = mkLogger(__name__, INFO)


r_SecStart = re.compile(r'^(?P<spaces> *)\[?(?P<name>"?[0-9A-Za-z_]+"?)\]? = $', re.M)

def dummy(*args, **kwargs):
    pass

class SLPP:

    @logged
    def __init__(self):
        self.text = ''
        self.ch = ''
        self.at = 0
        self.len = 0
        self.depth = 0
        self.space = re.compile('\s', re.M)
        self.alnum = re.compile('\w', re.M)
        self.reg_newline = re.compile('\n', re.M)
        self.newline = '\n'
        self.tab = '\t'

    @logged
    def decode(self, text):
        """
        Initialise le décodage d'un fichier mission

        La fonction va vérifier qu'elle a bien reçu une String en
        paramètre, la splitter sur base de newline, vérifier que le texte
        reçu est bien un fichier mission valide, et enfin lancer le parser
        sur le tableau obtenu
        """
        self.logger.info("début du décodage")
        if type(text) is not str:
            raise Exceptions.ParameterInvalid("", self.logger, "le paramètre passé n'est pas une string (type: {})".format(type(text)))
        self.lines = text.split("\n")
        self.line, self.at, self.len = self.lines[0], 0, len(self.lines)
        self.logger.debug("décodage préliminaire terminé, le fichier contient {} lignes".format(self.len))
        self.logger.debug('début du parsing des lignes')

        # Vérification de la validité du fichier mission
        self.logger.debug("première ligne: {}".format(self.line))
        r_firstLine = re.compile(r'^mission = $', re.M)
        r_secondLine = re.compile(r'^{$', re.M)
        if not r_firstLine.match(self.lines[0]):
            raise Exceptions.InvalidMissionFile(logger=self.logger, message="la première ligne du fichier mission est invalide")
        elif not r_secondLine.match(self.lines[1]):
            raise Exceptions.InvalidMissionFile(logger=self.logger, message="la seconde ligne du fichier mission est invalide")

        # Si tout est en ordre, démarrage du parsing
        self.logger.debug("tout est en ordre, début du parsing")
        result = self.__section()
        self.logger.info("fin du décodage")
        return result

    def nextLine(self):
        """
        Assigne la ligne suivante à la valeur de self.line

        Tant qu'il reste des lignes à parser, la fonction retourne True.
        Une fois la fin tu tableau atteinte, la fonction retourne None,
        ce qui permet de l'utiliser dans une boucle.
        """
        if self.at < self.len - 1:
##            if self.at != 0:
##                self.fallback(100 / (self.len / self.at))
            self.at += 1
            self.line = self.lines[self.at]
            logger.debug("nouvelle ligne: {}".format(self.at))
            return True
        logger.debug("dernière ligne atteinte")
        return None

    def __section(self):
        """
        Parse de façon réursive l'ensemble du tableau de lignes

            L'objet "section" (et je dis ici objet section, mais il ne s'agit
        que d'une fonction avec son namespace propre, d'ou les variables
        locales utilisées) aura comme "attributs" o, son dictionnaire de
        données, ident, qui représente l'identation des lignes de fin et
        de début de section, contentIdent, qui représente l'identation
        des lignes DANS la section, et name, qui sera le nom de la section.

            Une fois dans la section, la fonction traite quatre types de
        lignes, de façon atomique:

        1. Un début de section

            Un début de section doit correspondre à la regexp statique suivante:

        re.compile(r'^(?P<spaces> *)\[?(?P<name>"?[0-9A-Za-z_]+"?)\]? = $', re.M)

        décomposée comme suit:
            ^: une nouvelle ligne commence
            (?P<spaces> *): il y a un nombre indéterminé d'espaces, ou aucun
            \[?: il est possible que le caractère "[" suive les espaces
            (?P<name>"?[0-9A-Za-z_]*"?): le nom est composé de:
                "?: un guillement facultatif en entrée
                [0-9A-Za-z_]+: au moins un caractère alphanumérique/underscore
                "?: un guillement sortant facultatif
            \]?: le crochet fermant facultatif
             = $: un signe égale entouré de deux espaces, dont le dernier précède la fin de ligne

            Si un début de section est détecté, la fonction fera récursivement
        appel à elle-même pour le traiter.

        2. Une fin de section

            Une fin de section est caractérisée par la regexp dynamique suivante:

        re.compile('^{}\\}}, -- end of \\[{}\\]$'.format(ident, name))

        décomposée comme suit:
            ^: une nouvelle ligne commence
            {}: correspondra à l'identation de la section via format
            \\}}: deviendra un simple }, qui signifie fin de la section
            , -- end of: commun à toutes les sections
            \\[{}\\]: prendra comme valeur le nom de la section, déduit
            via format, et inclus entre crochets
            $: fin de ligne
            Remarques:
                - les \\ sont de simple \ échappés; cela m'évite d'avoir
                recours au raw strings (r'')
                - les crochets ouvrants ({{) et fermants (}}) sont doublés,
                du fait de l'utilisation de .format()

            Une fois la fin de section atteinte, le dictionnaire
        assemblé au cours du parsing est renvoyé, et est soit inclus au
        dictionaire de la section parente, soit renvoyé directement à la
        fonction decode(), ce qui marque la fin du parsing.

        3. Un paramètre sur une ligne

            Une paramètre sur une seule ligne est détecté viua la regexp
        dynamique suivant:

        re.compile('^{}\\[(?P<param>.*)\\] = (?P<value>.+),$'.format(contentIdent), re.M)

        décomposée comme suit:
        ^: début de ligne
        {}: deviendra l'identation du contenu de la section via .format()
        \\[: deviendra un simple crochet ouvrant
        (?P<param>.+): tout caractère entre crochet deviendra le "nom"
                        du paramètre
        \\] = : après le nom du paramètre, on trouve le crochet fermant,
                puis le signe égal entouré d'espaces.
        (?P<value>.+): tout caractère suivant l'espace d'après le signe
                        égal sera considéré comme la valeur du paramètre
        ,$: sauf pour la virgule de fin et la fin de ligne, qui signifie
            la fin du paramètre

        4. Un paramètre sur plusieurs lignes

            Le programme fait la différence entre les paramètre multilignes
        et les paramètres réguliers très simplement: si un paramètre régulier
        est détecté, la boucle continue sans passer par l'évaluation de
        la regexp de paramètre multiligne, qui est la suivante:

        re.compile('^{}\\[(?P<param>.+)\\] = (?P<value>".+)$'.format(contentIdent), re.M)

        et se décompose comme celle des paramètres réguliers, à l'exception
        de la virgule en fin de ligne, qui n'est pas présente dans un paramètre
        multilignes. Les lignes sont ensuites passée en revue au moyen d'une
        boucle While, en les ajoutant à chaque fois à la valeur du paramètre,
        jusqu'à tomber sur la ligne qui marque la fin du paramètre multilignes,
        désignée par la regexp:

        re.compile('^(?P<value>.+"),$'.format(contentIdent), re.M)

        qui se décompose comme suit:
        ^:début de ligne
        (?P<value>.+"): tout caractère, incluant un guillement obligatoire
                        à la fin, fait partie de la valeur du paramètre.
        ,$: la ligne doit se terminer par une virgule non incluse dans les
            guillemets
        """
        self.logger.debug("instanciation d'une nouvelle section")
##        o = {}
        o = OrderedDict()
        # Identations propres à cette section
        ident = r_SecStart.search(self.line).group("spaces")
        contentIdent = "    {}".format(ident)
        # Nom de la section
        name = r_SecStart.search(self.line).group("name")
        # Compilation de la regexp de fin de section
        r_end = re.compile('^{}\\}}, -- end of \\[{}\\]$'.format(ident, name))
        if name == "mission":
            r_end = re.compile('^\\}} -- end of mission'.format(ident, name))
        self.logger.debug('nouvelle section: {}\n\tindentation: "{}"\n\tindentation du contenu: "{}"\n\tfin de section: {}'.format(name, ident, contentIdent, r_end.pattern))
        # Check de validité
        self.nextLine()
        self.logger.debug("vérification du crochet ouvrant en début de section")
        r_check = re.compile('^{}{{$'.format(ident))
        if not r_check.match(self.line):
            raise Exceptions.InvalidMissionFile("mission passée en tant que texte", self.logger, "il manque le crochet ouvrant en début de section")
        # Compilation des regexp pour les paramètres
        self.logger.debug("compilation des expressions régulières pour le parsing")
        r_param = re.compile('^{}\\[(?P<param>.+)\\] = (?P<value>.+),$'.format(contentIdent), re.M)
        r_MLPstart = re.compile('^{}\\[(?P<param>.+)\\] = (?P<value>".+)$'.format(contentIdent), re.M)
        r_MLPend = re.compile('^(?P<value>.*"),$'.format(contentIdent), re.M)
        self.logger.debug("expressions régulières compilées:\n\tparamètre: {}\n\tdébut de paramètre multi-lignes: {}\n\tfin de paramètre multi-lignes: {}".format(
                        r_param.pattern, r_MLPstart.pattern, r_MLPend.pattern))
        # Parsing du contenu de la section
        self.logger.debug("tout semble en ordre, parsing de la section")
        while self.nextLine():
            # Ligne de paramètres trouvées
            if r_param.match(self.line):
                pName = r_param.search(self.line).group("param")
                pValue = r_param.search(self.line).group("value")
                #~ self.logger.debug("paramètre trouvé: {}\n\tValeur: {}".format(pName, pValue))
                self.logger.debug("paramètre trouvé: {} (ligne: {})\n\tvaleur: {}".format(pName, self.at, pValue))
                o[pName] = pValue
                continue
            # Paramètres multi lignes trouvé
            if r_MLPstart.match(self.line):
                pName = r_MLPstart.search(self.line).group("param")
                pValue = r_MLPstart.search(self.line).group("value")
                self.logger.debug("paramètre multilignes trouvé: {} (ligne: {})".format(name, self.at))
                self.nextLine()
                while not r_MLPend.match(self.line):
                    pValue = "\n".join([pValue, self.line])
                    self.logger.debug("nouvelle ligne trouvée pour le paramètre multi-ligne\n\tvaleur: {}".format(pValue))
                    self.nextLine()
                pValue = "\n".join([pValue, r_MLPend.search(self.line).group("value")])
                self.logger.debug("fin du paramètre multi-lignes trouvées\n\tvaleur: {}".format(pValue))
                o[pName] = pValue
                continue
            # Fin de section atteinte
            if r_end.match(self.line):
                #~ self.logger.debug("section {}: fin de section atteinte".format(name))
                self.logger.debug("fin de la section atteinte, renvoi du dictionaire créé")
                return o
            # Début de nouvelle section
            if r_SecStart.match(self.line):
                newSecName = r_SecStart.search(self.line).group("name")
                self.logger.debug("sous-section trouvée, récursion")
                o[newSecName] = self.__section()
        #~ self.logger.error("section mal formattée: {}".format(name))
        raise Exceptions.InvalidMissionFile("", self.logger, "section mal formattée: {}, ligne {}".format(name, self.at))

    @logged
    def encode(self, obj, total=0):
        """
        Ecrit un dictionnaire de données dans un fichier mission

        Cette fonction sert de coquille (wrapper) à la fonction de plus
        bas niveau __encode(). Ici, on va poser les bases, c'est-a-dire
        les première, seconde et dernière lignes du fichier mission.
        Toutes les lignes de données qui se trouvent entre ces trois-là
        seront extraite du dictionnaire par __encode().
        """
        self.logger.info("début de l'encodage")
        self.count = 0
        self.total = total
        self.logger.debug("début de l'encodage")
        if not obj:
            raise Exceptions.EncodingError("aucun objet passé en paramètre", self.logger)
        self.depth = 0
        self.logger.debug("écriture de la première ligne")
        self.text = 'mission = \n{\n'
        self.logger.debug("encodage des sections")
        self.__encode(obj)
        self.logger.debug("écriture de la dernière ligne")
        self.text = ''.join([self.text, '} -- end of mission\n'])
        self.logger.debug("renvoi du texte créé")
        self.logger.info("fin de l'encodage")
        return self.text

    def __encode(self, obj):
        """
        Cette fonction itère au travers du dictionnaire de données pour
        extraire toutes les sections et paramètres à écrire dans le nouveau
        fichier mission. Le formats de débuts et de fins de sections utilisés par la série
        DCS sont respectés.
        """
        self.count += 1
##        self.fallback(100 / (self.total / self.count))
        self.logger.debug("début de l'encodage des sections")
        self.depth += 1
        self.logger.debug("profondeur actuelle: {}".format(self.depth))
        ident = ' ' * 4 * self.depth
        self.logger.debug('indentation: "{}"'.format(ident))
        self.logger.debug("itération des objets dans la section")
        for key in obj.keys():
            self.logger.debug("encodage de {}".format(key))
            if type(obj[key]) == str:
                self.count += 1
##                self.fallback(100 / (self.total / self.count))
                self.logger.debug("l'objet est une chaine de caractère, valeur: {}".format(obj[key]))
                s = ''.join([ident, "[", key, "]", " = ", obj[key], ",\n"])
                self.logger.debug('la ligne ajoutée au fichier sera: "{}"'.format(s))
                self.text = ''.join([self.text, s])
##            elif type(obj[key]) == dict:
            elif type(obj[key]) == OrderedDict:
                self.logger.debug("l'objet est une section")
                s = ''.join([ident, "[", str(key), "]", " = \n", ident, "{\n"])
                self.logger.debug('début de section à ajouter au fichier: "{}"'.format(s))
                self.text = ''.join([self.text, s])
                self.logger.debug("récursion pour l'encodage du contenu de la section")
                self.__encode(obj[key])
                self.logger.debug("contenu de section encodé, fermeture de la section")
                self.text = ''.join([self.text, ident, "}}, -- end of [{}]\n".format(key)])
        self.depth -= 1
        self.logger.debug("profondeur actuelle: {}".format(self.depth))

_slpp = SLPP()

__all__ = ['_slpp']
