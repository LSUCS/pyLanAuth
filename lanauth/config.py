from configparser import ConfigParser, ParsingError, NoSectionError

from lanauth import project


class SiteConfig(ConfigParser):
    """Configuration options for the site.
    Raises exceptions if the required sections are missing
    """
    required_sections = ['flask', 'database', 'lan_api', 'device']


    @classmethod
    def from_file(cls, filename):
        conf = SiteConfig(default_section=project)
        if not conf.read([filename]):
            raise ParsingError("Failed to parse file: %s" % filename)

        # Check sections
        for section in cls.required_sections:
            if not conf.has_section(section):
                raise NoSectionError("Missing section: %s" % section) 

        return conf



# test
if __name__ == '__main__':
    import sys
    print("Reading config: %s" % sys.argv[1])
    conf = SiteConfig.from_file(sys.argv[1])
    if conf is None:
        print("Error reading config")

    print("Reading attrs")
    for section in conf.sections():
        for key,item in getattr(conf, section).items():
            print("%s:%s" % (key, item))
    


