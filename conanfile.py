from conans import ConanFile, CMake, tools


class LibzmqConan(ConanFile):
    name = "libzmq"
    version = "4.2.2"
    license = "BSD"
    url = "https://github.com/cinderblocks/conan-libzmq"
    description = "ZeroMQ core engine in C++, implements ZMTP/3.0"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=False"
    generators = "cmake"

    def source(self):
        self.run("git clone https://github.com/zeromq/libzmq.git")
        self.run("cd libzmq && git checkout tags/v4.2.2")

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
