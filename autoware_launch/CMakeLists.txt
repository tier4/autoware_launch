cmake_minimum_required(VERSION 3.5)
project(autoware_launch)

find_package(ament_cmake_auto REQUIRED)
ament_auto_find_build_dependencies()

if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  ament_lint_auto_find_test_dependencies()
endif()

# Install the AWF-tracked `config/` as `config_lv4/`, and `config_lv2/` as-is,
# then create a `config -> config_lv4` symlink as the default switch target.
# Launch files resolve `$(find-pkg-share autoware_launch)/config/...`, so the
# symlink keeps that path stable while letting us swap the link target between
# config_lv4 and config_lv2 (manually for now; via a script in the future).
install(DIRECTORY config/ DESTINATION share/${PROJECT_NAME}/config_lv4)
install(DIRECTORY config_lv2 DESTINATION share/${PROJECT_NAME})

install(CODE
  "set(_link \"\$ENV{DESTDIR}\${CMAKE_INSTALL_PREFIX}/share/${PROJECT_NAME}/config\")
   if(NOT EXISTS \"\${_link}\" AND NOT IS_SYMLINK \"\${_link}\")
     execute_process(COMMAND \${CMAKE_COMMAND} -E create_symlink config_lv4 \"\${_link}\")
   endif()"
)

ament_auto_package(
  INSTALL_TO_SHARE
  launch
  rviz
)
