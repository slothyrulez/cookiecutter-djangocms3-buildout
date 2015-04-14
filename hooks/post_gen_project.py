#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Post hooks to finish install

When developing on this script, add "test" as first argument to use test mode with 
a dummy context else the script will fails (because the context is empty).
"""
import ast, json, os

# Capture cookiecutter context
COOKIE_CONTEXT = """{{ cookiecutter }}"""

# A sample of cookiecutter context used for test/dev purposes
TEST_CONTEXT = {
    "project_name": "Project name", 
    "author_email": "support@emencia.com", 
    "author_name": "Emencia", 
    "version": "0.1.0", 
    "repo_name": "project-name",
    "github_username": "emencia", 
    "secret_key": "DUMMY-KEY", 
    "enable_accounts": "yes", 
    "enable_contact_form": "no", 
    "enable_porticus": "yes", 
    "enable_slideshows": "yes", 
    "enable_socialaggregator": "no", 
    "enable_zinnia": "yes"
}


class AppManager(object):
    """
    Manage apps from given context
    """
    # Base apps are always enabled
    BASE_APPS = [
        'admin_style',
        'assets', # Used in templates
        'ckeditor', # Used in djangocms and another apps
        'cms',
        'emencia_utils', # Useful utilities
        'filebrowser', # Used in djangocms and another apps
        'google_tools', # Used for almost customer projects
        'site_metas', # Common sitemap for djangocms and another apps
        'sitemap', # Common sitemap for djangocms and another apps
    ]

    # Optional apps enabled if their context value is "yes"
    # Key is the prompt question variable name, Value is the app name to add
    OPTIONAL_APPS = {
        'enable_accounts': 'accounts',
        'enable_contact_form': 'contact_form',
        'enable_porticus': 'porticus',
        'enable_slideshows': 'slideshows',
        'enable_socialaggregator': 'socialaggregator',
        'enable_zinnia': 'zinnia',
    }

    # Dependancies that will be added to enabled apps if their dependant is enabled
    # Key is the app name, Value is a list of app names to add
    DEPENDANCIES = {
        'accounts': ['crispy_forms', 'recaptcha'],
        'contact_form': ['crispy_forms', 'recaptcha'],
    }
    def __init__(self, context, test_mode=False):
        self.context = context
        self.test_mode = test_mode

    def get_enabled_apps(self):
        """
        Return a list of all enabled apps from base apps, optional apps, 
        dependancies, etc..
        """
        apps = [k for k in self.BASE_APPS]
        
        # Search for optional app variable name in context
        for varname,appname in self.OPTIONAL_APPS.items():
            if varname in self.context and self.context.get(varname) == 'yes':
                apps.append(appname)
        
        # Search for dependancies
        for item in apps:
            if item in self.DEPENDANCIES:
                apps.extend(self.DEPENDANCIES.get(item))
        
        return set(apps)

    def enable_mods(self, apps):
        """
        Enable mods in their dependancies from enabled apps
        """
        mods = set(apps)
        symlink_list = []
        project_dir = './project'
        
        # Build a list of symlink to create for mods
        symlink_list = [(
            os.path.join('..', 'mods_available', name),
            os.path.join(project_dir, 'mods_enabled', name)
        ) for name in mods]
        
        #print json.dumps(symlink_list, indent=4)
        
        # Create symlinks
        for target, linkfile in symlink_list:
            print "* Symlink TO:", target, 'INTO:', linkfile
            if not self.test_mode:
                os.symlink(target, linkfile)
        
        return symlink_list


def print_part_title(title):
    print "="*len(title)
    print title
    print "="*len(title)
    print

if __name__ == "__main__":
    import sys
    # Get the context to use and enable or not the test mode
    test_mode = False
    if len(sys.argv)>1 and sys.argv[1].strip() == 'test':
        context = TEST_CONTEXT
        test_mode = True
    else:
        context = ast.literal_eval(COOKIE_CONTEXT)
        
    print_part_title("Enable mods")
    apm = AppManager(context, test_mode)
    apps = apm.get_enabled_apps()
    apm.enable_mods(apps)
    print
    
    #print_part_title("Init Git repository")
    #print "TODO"
    #print
    
    #print_part_title("Go ahead")
    #print "Your new project should be ready now."
    #print
    #print "Just enter to 'foo' directory then launch the following command to install it:"
    #print
    #print "    make install"
    #print