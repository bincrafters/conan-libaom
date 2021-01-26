from conans import ConanFile, CMake, tools
from conans.errors import ConanInvalidConfiguration
from conans.tools import Version
import os


class LibnameConan(ConanFile):
    name = "libaom"
    version = "1.0.0"
    description = "Keep it short"
    topics = ("libaom", "media","encoding")
    url = "https://github.com/bincrafters/conan-libaom"
    homepage = "https://aomedia.googlesource.com/aom"
    license = "BSD-2-Clause-FreeBSD"
    exports_sources = ["CMakeLists.txt"]
    generators = "cmake"

    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}

    _source_subfolder = "source_subfolder"
    _build_subfolder = "build_subfolder"
    _cmake = None

    def configure(self):
        compiler_version = Version(self.settings.compiler.version.value)
        if self.settings.os == "Windows" and self.options.shared:
          raise ConanInvalidConfiguration("Windows DLL builds not supported yet")
        if self.settings.compiler == "Visual Studio" and compiler_version < "15":
          raise ConanInvalidConfiguration("Visual Studio 2015 and earlier aren't supported")

    def config_options(self):
        if self.settings.os == 'Windows':
            del self.options.fPIC

    def source(self):
        os.makedirs(self._source_subfolder)
        with tools.chdir(self._source_subfolder):
            download_source = "https://download.videolan.org/contrib/aom/"
            tools.get("{0}/aom-v{1}.errata.1.tar.gz".format(download_source, self.version), sha256="a4abc492a455d83869da28096bd0e807b949769d0cc38c5489ff04aac4fc7724")

    def _configure_cmake(self):
        if not self._cmake:
            cmake = CMake(self, set_cmake_flags=True)
            cmake.definitions["ENABLE_TESTS"] = False
            cmake.definitions["ENABLE_TESTDATA"] = False
            cmake.definitions["ENABLE_EXAMPLES"] = False
            cmake.definitions["ENABLE_DOCS"] = False
            cmake.definitions["ENABLE_TOOLS"] = False
            cmake.definitions["AOM_BUILD_CMAKE_MSVC_RUNTIME_CMAKE_"] = 1
            cmake.configure(build_folder=self._build_subfolder)
            self._cmake = cmake
        return self._cmake

    def build(self):
        cmake = self._configure_cmake()
        cmake.build()

    def package(self):
        self.copy(pattern="LICENSE", dst="licenses", src=self._source_subfolder)
        if self.settings.compiler == "Visual Studio":
            self.copy(pattern="*.h", src=os.path.join(self._source_subfolder, "aom"), dst=os.path.join("include", "aom"))
            self.copy(pattern="*.lib", src=".", dst="lib", keep_path=False)
            self.copy(pattern="*.dll", src=".", dst="bin", keep_path=False)
        else:
            cmake = self._configure_cmake()
            cmake.install()

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
