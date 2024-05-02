from django.core.files.storage import FileSystemStorage

class OverwriteStorage(FileSystemStorage):
	def get_available_name(self, name: str, max_length: int = None) -> str:
		self.delete(name)
		return name