from .constants import FORWARDS


class Applier:

    def __init__ (self, ruleset):
        """Initialises this Applier.

        :param ruleset: the ruleset this applier will use for
          transformations
        :type ruleset: `.Ruleset`

        """
        self._ruleset = ruleset

    def _apply_rule (self, word, rule):
        """Returns a new word resulting from transforming `word` using
        `rule`.

        :param word: word to be transformed
        :type word: `.Word`
        :param rule: rule to apply to `word`
        :type rule: `.Rule`
        :rtype: `.Word`

        """
        reg_exp = rule.applier_form
        result = reg_exp.subn(self._modify_features, word.normalised_form)
        result_word = ''
        return result_word
        
    def _transform_word (self, word, rules):
        """Transforms `word`.

        :param word: word to transform
        :type word: `.Word`
        :param rules: rules to transform word with
        :type rules: `list` of `.Rule`s

        """
        for rule in rules:
            transformed_word = self._apply_rule(word, rule)
            next_rules = rule.get_next_rules()
            self._transform_word(transformed_word, next_rules)
    
    def transform_lexicon (self, lexicon):
        """Transforms and returns the words in `lexicon`.

        This method is a generator that yields each word in `lexicon`,
        annotated with the results of the transformation.

        :param lexicon: words to be transformed
        :type lexicon: `list` of `.Word`\s

        """
        for word in lexicon:
            rules = self._ruleset.get_rules(word.language, word.date,
                                            FORWARDS)
            self._transform_word(word, rules)
            yield word
