resource "yandex_storage_bucket" "b354575785676456" {
  bucket = "my-policy-bucket1234"

  anonymous_access_flags {
    read = true
    list = false
  }
}