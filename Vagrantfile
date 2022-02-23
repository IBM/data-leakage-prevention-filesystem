Vagrant.configure("2") do |config|
  config.vm.box = "ubuntu/xenial64"
  config.vm.network "forwarded_port", guest: 8888, host: 8888

  # config.vm.box_check_update = false

  config.vm.provider "virtualbox" do |vb|
    # Display the VirtualBox GUI when booting the machine
    vb.gui = false

     # Customize the amount of memory on the VM:
     vb.memory = "1024"
  end
  # config.vm.provision "shell", inline: <<-SHELL
  #   apt-get update
  #   apt-get install -y python3-pip
  #   pip3 install jupyter
  #   git clone https://github.com/google/re2.git && cd re2 && make && make test && sudo make install && sudo make testinstall
  #   pip3 install pybind11
  #   CFLAGS='-std=c++11' pip3 install --global-option=build_ext --global-option="-L/usr/local/lib" --global-option="-R/usr/local/lib" google-re2
  #   pip3 install pandas
  #   pip3 install -e /vagrant/
  # SHELL
  # config.vm.provision :shell, privileged: false, run: 'always', inline: <<-SHELL
  #   #cd /vagrant && jupyter notebook --ip 0.0.0.0 --no-browser --NotebookApp.token='' --NotebookApp.password='' &
  #   #cd /vagrant && mkdir -p loopback && python3 -m ppfs -r input/ -m loopback/ -t loopback &
  #   #cd /vagrant && mkdir -p protected-re && python3 -m ppfs -r input/ -m protected-re/ -t ppfs -s example-rules.json &
  #   #cd /vagrant && mkdir -p protected-re2 && python3 -m ppfs -r input/ -m protected-re2/ -t ppfs -s example-rules.json -re2 &
  # SHELL
end
