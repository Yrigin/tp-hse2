import pytest
from pathlib import Path
from tempfile import TemporaryDirectory
from src.media_indexing.folder_index import ( 
    get_artist,
    remove_artist,
    Media,
    Folder,
    get_folders,
    get_folder_files,
    get_updated_media_paths,
    apply_new_media_paths,
    reindex_folders,
    VARIOUS_ARTISTS_NAME
)

# Тесты для get_artist
def test_get_artist():
    assert get_artist("[Artist]") == "Artist"
    # assert get_artist("[Artist Name]") == "Artist Name ff"
    assert get_artist("No artist") is None

    with pytest.raises(ValueError):
            get_artist("[artist1][artist2]")

    

    
    # assert get_artist("[artist1][artist2]") is None  # или должно вызывать исключение?
    # assert get_artist("[Various Artists]") == VARIOUS_ARTISTS_NAME

# Тесты для remove_artist
def test_remove_artist():
    assert remove_artist("[Artist] Song") == "Song"
    assert remove_artist("Song [Artist]") == "Song"
    assert remove_artist("No artist") == "No artist"
    assert remove_artist("[Artist]") == ""

# Тесты для Media
def test_media():
    with TemporaryDirectory() as tmpdir:
        path = Path(tmpdir) / "test [Artist].mp3"
        path.touch()
        media = Media(path)
        
        assert media.artist_name == "Artist"
        assert media.title == "test"
        
        media.rename_update()
        assert media.path.name == "test [Artist].mp3"

# Тесты для Folder
def test_folder():
    with TemporaryDirectory() as tmpdir:
        # Создаем тестовую папку с файлами
        folder_path = Path(tmpdir) / "Test Folder"
        folder_path.mkdir()
        
        # Создаем несколько медиафайлов
        (folder_path / "song1 [Artist1].mp3").touch()
        (folder_path / "song2 [Artist2].mp3").touch()
        
        folder = Folder(folder_path)
        
        assert folder.title == "Test Folder"
        assert folder.get_counter() == 2
        assert len(folder.get_media_list()) == 2
        
        folder.rename_with_counter()
        assert folder.path.name == "Test Folder (2)"

# Тесты для get_folders и get_folder_files
def test_get_folders_and_files():
    with TemporaryDirectory() as tmpdir:
        # Создаем несколько папок
        folders = ["Folder1", "Folder2", ".hidden"]
        for folder in folders:
            (Path(tmpdir) / folder).mkdir()
        
        # Проверяем получение папок
        found_folders = get_folders(Path(tmpdir))
        assert len(found_folders) == 2  # .hidden должен быть пропущен
        
        # Проверяем получение файлов
        test_folder = Path(tmpdir) / "Folder1"
        (test_folder / "file1.txt").touch()
        (test_folder / "file2.txt").touch()
        
        files = get_folder_files(test_folder)
        assert len(files) == 2

# Тесты для get_updated_media_paths и apply_new_media_paths
def test_media_reorganization():
    with TemporaryDirectory() as tmpdir:
        base_dir = Path(tmpdir)
        
        # Создаем тестовую структуру
        folder1 = base_dir / "Folder1"
        folder1.mkdir()
        (folder1 / "song1 [Artist1].mp3").touch()
        (folder1 / "song2 [Artist2].mp3").touch()
        
        folder2 = base_dir / "Folder2"
        folder2.mkdir()
        (folder2 / "song3.mp3").touch()  # без артиста
        
        # Получаем маппинг
        mapping = get_updated_media_paths(base_dir)
        assert len(mapping) == 3
        
        # Применяем изменения
        apply_new_media_paths(mapping)
        
        # Проверяем результат
        assert (base_dir / "Artist1").exists()
        assert (base_dir / "Artist2").exists()
        assert (base_dir / VARIOUS_ARTISTS_NAME).exists()
        assert not folder1.exists()  # должна быть удалена, так как пустая
        assert not folder2.exists()  # должна быть удалена, так как пустая

# Тест для reindex_folders
def test_reindex_folders():
    with TemporaryDirectory() as tmpdir:
        base_dir = Path(tmpdir)
        
        # Создаем тестовую структуру
        folder = base_dir / "Folder"
        folder.mkdir()
        (folder / "song1 [Artist].mp3").touch()
        (folder / "song2 [Artist].mp3").touch()
        
        folders = get_folders(base_dir)
        reindex_folders(folders)
        
        # Проверяем результат
        assert (base_dir / "Folder (2)").exists()
        for media_file in (base_dir / "Folder (2)").iterdir():
            assert "[Artist]" in media_file.name