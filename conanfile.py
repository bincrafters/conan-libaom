# -*- coding: utf-8 -*-

from conans import ConanFile, CMake, tools
import os


class LibnameConan(ConanFile):
    name = "libaom"
    version = "1.0.0"
    description = "Keep it short"
    # topics can get used for searches, GitHub topics, Bintray tags etc. Add here keywords about the library
    topics = ("conan", "libaom", "media","encoding")
    url = "https://github.com/bincrafters/conan-libaom"
    homepage = "https://aomedia.googlesource.com/aom"
    author = "Bincrafters <bincrafters@gmail.com>"
    license = "BSD-2-Clause-FreeBSD"  # Indicates license type of the packaged library; please use SPDX Identifiers https://spdx.org/licenses/
    exports = ["LICENSE.md"]      # Packages the license for the conanfile.py
    # Remove following lines if the target lib does not use cmake.
    exports_sources = ["CMakeLists.txt"]
    generators = "cmake"

    # Options may need to change depending on the packaged library.
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}

    # Custom attributes for Bincrafters recipe conventions
    _source_subfolder = "source_subfolder"
    _build_subfolder = "build_subfolder"

    def config_options(self):
        if self.settings.os == 'Windows':
            del self.options.fPIC

    def source(self):
        download_source = "https://download.videolan.org/contrib/aom/"
        tools.get("{0}/aom-v{1}.errata.1.tar.gz".format(download_source, self.version), sha256="a4abc492a455d83869da28096bd0e807b949769d0cc38c5489ff04aac4fc7724")
        extracted_dir = self.name + "-" + self.version

        # Rename to "source_subfolder" is a convention to simplify later steps
        #os.rename(extracted_dir, self._source_subfolder)

    def _configure_cmake(self):
        cmake = CMake(self)
        cmake.definitions["BUILD_TESTS"] = False  # example
        cmake.configure(build_folder=self._build_subfolder)
        return cmake

    def build(self):
        cmake = self._configure_cmake()
        cmake.build()

    def package(self):
        self.copy(pattern="LICENSE", dst="licenses", src=self._source_subfolder)
        cmake = self._configure_cmake()
        cmake.install()
        # If the CMakeLists.txt has a proper install method, the steps below may be redundant
        # If so, you can just remove the lines below
        self.copy(pattern="**/*.h", dst="include", src=self._source_subfolder)
        self.copy(pattern="*.dll", dst="bin", keep_path=False)
        self.copy(pattern="*.lib", dst="lib", keep_path=False)
        self.copy(pattern="*.a", dst="lib", keep_path=False)
        self.copy(pattern="*.so*", dst="lib", keep_path=False)
        self.copy(pattern="*.dylib", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
