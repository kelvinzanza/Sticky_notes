# posts/tests.py
from django.test import TestCase
from django.urls import reverse
from .models import Post, Author



class PostModelTest(TestCase):
    """Tests that will run"""
    def setUp(self):
        # Create an Author object
        author = Author.objects.create(name='Test Author')
        # Create a Post object for testing
        Post.objects.create(
            title='Test Post', content='This is a test post.', author=author
            )

    def test_post_has_title(self):
        # Test that a Post object has the expected title
        post = Post.objects.get(id=1)
        self.assertEqual(post.title, 'Test Post')

    def test_post_has_content(self):
        # Test that a Post object has the expected content
        post = Post.objects.get(id=1)
        self.assertEqual(post.content, 'This is a test post.')


class PostViewTest(TestCase):
    """Tests to run"""
    def setUp(self):
        # Create an Author object
        author = Author.objects.create(name='Test Author')
        # Create a Post object for testing views
        Post.objects.create(
            title='Test Post', content='This is a test post.', author=author
            )

    def test_post_list_view(self):
        # Test the post-list view
        response = self.client.get(reverse('post_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Post')

    def test_post_detail_view(self):
        # Test the post-detail view
        post = Post.objects.get(id=1)
        response = self.client.get(
            reverse('post_detail', args=[str(post.id)])
            )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Post')
        self.assertContains(response, 'This is a test post.')

class PostCreateTest(TestCase):
    def setUp(self):
        author = Author.objects.create(name='Test Author')
        Post.objects.create(
            title='Test Post', content='This is a test post.', author=author
            )
        
    def test_post_has_title(self):
        post = Post.objects.get(id=1)
        self.assertEqual(post.title, 'Test Post')

    def test_post_has_content(self):
        post = Post.objects.get(id=1)
        self.assertEqual(post.content, 'This is a test post.')

class PostUpdateTest(TestCase):
    def setUp(self):
        author = Author.objects.create(name='Test Author')
        self.post = Post.objects.create(
            title='Test Post', content='This is a test post.', author=author
            )
        
    def test_post_valid_update(self):
        updated_data = {
            "title": "Updated Title",
            "content": "Updated Content",
            "author": self.user.pk,
        }
        response = self.client.post(self.update_url, data=updated_data)
        self.assertRedirects(response, reverse("post_list"))
        self.post.refresh_from_db()
        self.assertEqual(self.post.title, "Updated Title")
        self.assertEqual(self.post.content, "Updated Content")


class PostDeleteTest(TestCase):
    def setUp(self):
        author = Author.objects.create(name='Test Author')
        self.post = Post.objects.create(
            title='Test Post', content='This is a test post.', author=author
            )
        self.delete_url = reverse('post_delete', args=[self.post.pk])
        
    def test_delete_post(self):
        response = self.client.get(self.delete_url)
        self.assertRedirects(response, reverse('post_list'))
        self.assertFalse(Post.objects.filter(pk=self.post.pk).exists())

    def test_post_delete_non_existent_post(self):
        non_existent_url = reverse('post_delete', args=[999])
        response = self.client.post(non_existent_url)
        self.assertEqual(response.status_code, 404)
