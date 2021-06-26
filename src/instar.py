#!/bin/python3.7

import subprocess
import os

def main():

  # Grab information

  a_path = input("Path to tar-archive >> ")
  if a_path == '':
    print("Program can't be installed from blank path")
  p_name = input("Short program name >> ")
  if p_name == '':
    print("Program name can't be blank.")
    exit(1)
  p_dir = input("Path to programs dir (with last '/') >> ")
  if p_dir == '':
    p_dir = "/etc/programs/"
  create_de = input("Create desktop entry (y/n) >> ") == 'y'
  de_name = ''
  de_version = ''
  de_gen_name = ''
  de_comment = ''
  de_icon = ''
  de_categories = ''
  if create_de:
    de_name = input("Desktop entry (DE) name >> ")
    de_version = input("DE version >> ")
    de_gen_name = input("DE generic name >> ")
    de_comment = input("DE comment >> ")
    de_icon = input("DE icon >> ")
    de_categories = input("DE categories (splitted by ';') >> ")

  # Extract program from archive
  subprocess.run(f"mkdir -p \"{p_dir}{p_name}\"", shell=True, check=True)
  subprocess.run(f"tar -xf \"{a_path}\" -C \"{p_dir}{p_name}\"", shell=True, check=True)
  f_list = os.listdir(f"{p_dir}{p_name}")
  if len(f_list) == 1:
    if os.path.isdir(f"{p_dir}{p_name}/{f_list[0]}"):
      tmp_name = "tmp0000000000000001"
      subprocess.run(
        f"mv \"{p_dir}{p_name}/{f_list[0]}\" \"{p_dir}{p_name}/{tmp_name}\"",
        shell=True,
        check=True
      )
      subprocess.run(
        f"mv {p_dir}{p_name}/{tmp_name}/* \"{p_dir}{p_name}/\"",
        shell=True,
        check=True
      )
      subprocess.run(
        f"rmdir \"{p_dir}{p_name}/{tmp_name}\"",
        shell=True,
        check=True
      )

  # Getting executable file name
  subprocess.run(f"ls --color -lah \"{p_dir}{p_name}\"", shell=True, check=True)
  exec_file = input("Executable file name >> ")
  exec_path = f"{p_dir}{p_name}"
  if exec_file != '':
    exec_path = f"{exec_path}/{exec_file}"

  # Create bash runner script
  subprocess.run(
    f"echo \"#!/bin/bash\n{exec_path}\" >> /usr/bin/{p_name}",
    shell=True,
    check=True
  )
  subprocess.run(
    f"chmod +x /usr/bin/{p_name}",
    shell=True,
    check=True
  )

  # Create desktop entry
  de_path = f"{p_dir}{p_name}/{p_name}.desktop"
  if os.path.isfile(de_path):
    print("Desktop entry already exist.")
  else:
    subprocess.run(
      f"echo \"[Desktop Entry]\n\" >> {de_path}",
      shell=True,
      check=True
    )
    subprocess.run(
      f"echo \"Type=Application\" >> {de_path}",
      shell=True,
      check=True
    )
    subprocess.run(
      f"echo \"Version={de_version}\" >> {de_path}",
      shell=True,
      check=True
    )
    subprocess.run(
      f"echo \"Name={de_name}\" >> {de_path}",
      shell=True,
      check=True
    )
    subprocess.run(
      f"echo \"GenericName={de_gen_name}\" >> {de_path}",
      shell=True,
      check=True
    )
    subprocess.run(
      f"echo \"Comment={de_comment}\" >> {de_path}",
      shell=True,
      check=True
    )
    subprocess.run(
      f"echo \"Exec={exec_path}\" >> {de_path}",
      shell=True,
      check=True
    )
    subprocess.run(
      f"echo \"Icon={de_icon}\" >> {de_path}",
      shell=True,
      check=True
    )
    subprocess.run(
      f"echo \"Categories={de_categories}\" >> {de_path}",
      shell=True,
      check=True
    )

    subprocess.run(
      f"ln -s {de_path} /usr/share/applications/",
      shell=True,
      check=True
    )

if __name__ == '__main__':
  main()
