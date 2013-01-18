import os

from name_gen.namegen import NameGen
import name_gen 

LANGUAGE = "russian"


name_lang_file = os.path.join(os.path.dirname(name_gen.__file__),
                              "Languages", "%s.txt" % LANGUAGE)
name_generator = NameGen(name_lang_file)


def generate_name():
    return name_generator.gen_word()
    