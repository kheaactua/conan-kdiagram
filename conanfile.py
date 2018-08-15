#!/usr/bin/env python
# -*- coding: future_fstrings -*-
# -*- coding: utf-8 -*-

import os
from conans import ConanFile, CMake, tools


class KdiagramConan(ConanFile):
    name            = 'kdiagram'
    version         = '2.6.1'
    license         = 'Qt'
    url             = 'https://github.com/kheaactua/conan-kdiagram'
    description     = 'Build kdiagram'
    settings        = 'os', 'compiler', 'build_type', 'arch'
    options         = {'shared': [True, False]}
    default_options = 'shared= False'
    generators      = 'cmake'

    requires = (
        'qt/[>5.6]@ntc/stable',
        'helpers/0.3@ntc/stable',
    )

    def configure(self):
        self.options['qt'].svg = True

    def source(self):
        self.run(f'git clone https://github.com/KDE/kdiagram {self.name}')
        self.run(f'cd {self.name} && git checkout v{self.version}')

    def build(self):

        from platform_helpers import adjustPath

        cmake = CMake(self)

        # Qt exposes pkg-config files (at least on Linux, on Windows there are
        # .prl files *shrugs*, but PCL (pcl_find_qt5.cmake) doesn't use this.
        qt_deps = ['Core', 'Gui', 'OpenGL', 'Widgets', 'Svg']
        for p in qt_deps:
            cmake.definitions[f'Qt5{p}_DIR:PATH'] = adjustPath(os.path.join(self.deps_cpp_info['qt'].rootpath, 'lib', 'cmake', f'Qt5{p}'))
        cmake.definitions['QT_QMAKE_EXECUTABLE:PATH'] = adjustPath(os.path.join(self.deps_cpp_info['qt'].rootpath, 'bin', 'qmake'))

        cmake.configure(source_folder=self.name)
        cmake.build()
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)

# vim: ts=4 sw=4 expandtab ffs=unix ft=python foldmethod=marker :
