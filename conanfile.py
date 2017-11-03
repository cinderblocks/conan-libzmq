from conans import ConanFile, CMake, tools


class LibzmqConan(ConanFile):
    name = "libzmq"
    version = "4.2.2"
    license = "BSD"
    url = "<Package recipe repository url here, for issues about the package>"
    description = "ZeroMQ core engine in C++, implements ZMTP/3.0"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=False"
    generators = "cmake"

    def source(self):
        self.run("git clone https://github.com/zeromq/libzmq.git")
        self.run("cd libzmq && git checkout tags/v4.2.2")
        # This small hack might be useful to guarantee proper /MT /MD linkage in MSVC
        # if the packaged project doesn't have variables to set it properly
        tools.replace_in_file("libzmq/CMakeLists.txt", "PROJECT(libzmq)", '''PROJECT(libzmq)
include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()''')

    def build(self):
        cmake = CMake(self)
        self.run('cmake libzmq %s' % cmake.command_line)
        self.run("cmake --build . %s" % cmake.build_config)

    def package(self):
        self.copy("*.h", dst="include", src="libzmq/include")
        self.copy("*.lib", dst="lib", keep_path=False)
        self.copy("*.dll", dst="bin", keep_path=False)
        self.copy("*.so", dst="lib", keep_path=False)
        self.copy("*.dylib", dst="lib", keep_path=False)
        self.copy("*.a", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
