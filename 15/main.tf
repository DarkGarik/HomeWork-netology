terraform {
  required_providers {
    yandex = {
      source = "yandex-cloud/yandex"
    }
  }
  required_version = ">= 0.13"
}

provider "yandex" {
  folder_id = "${var.yc_folder_id}"
  zone = "ru-central1-a"
}

resource "yandex_vpc_network" "netology-net" {
  name = "netology-network"
}

resource "yandex_vpc_subnet" "public" {
  v4_cidr_blocks = ["192.168.10.0/24"]
  network_id     = "${yandex_vpc_network.netology-net.id}"
  name = "public"
}

resource "yandex_vpc_subnet" "private" {
  v4_cidr_blocks = ["192.168.20.0/24"]
  network_id     = "${yandex_vpc_network.netology-net.id}"
  name = "private"
  route_table_id = "${yandex_vpc_route_table.netology-route.id}"
}

resource "yandex_vpc_route_table" "netology-route" {
  network_id = "${yandex_vpc_network.netology-net.id}"
  name = "net-route"

  static_route {
    destination_prefix = "0.0.0.0/0"
    next_hop_address   = "192.168.10.254"
  }
}

resource "yandex_compute_instance" "nat" {
  name = "nat-netology"

  resources {
    cores  = 2
    memory = 2
  }

  boot_disk {
    initialize_params {
      image_id = "fd8o8aph4t4pdisf1fio"
    }
  }

  network_interface {
    subnet_id = "${yandex_vpc_subnet.public.id}"
    ip_address = "192.168.10.254"
    nat       = true
  }

  metadata = {
    ssh-keys = "ubuntu:${file("~/.ssh/id_rsa.pub")}"
  }
}

resource "yandex_compute_instance" "vm1" {
  name = "vm1"

  resources {
    cores  = 2
    memory = 2
  }

  boot_disk {
    initialize_params {
      image_id = "fd8smb7fj0o91i68s15v"
    }
  }

  network_interface {
    subnet_id = "${yandex_vpc_subnet.public.id}"
    nat = true
  }

  metadata = {
    ssh-keys = "ubuntu:${file("~/.ssh/id_rsa.pub")}"
  }
}

resource "yandex_compute_instance" "vm2" {
  name = "vm2"

  resources {
    cores  = 2
    memory = 2
  }

  boot_disk {
    initialize_params {
      image_id = "fd8smb7fj0o91i68s15v"
    }
  }

  network_interface {
    subnet_id = "${yandex_vpc_subnet.private.id}"
  }

  metadata = {
    ssh-keys = "ubuntu:${file("~/.ssh/id_rsa.pub")}"
  }
}