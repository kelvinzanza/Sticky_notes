# posts/tests.py
from django.test import TestCase
from django.urls import reverse
from .models import Post, Author


class PostModelTest(TestCase):
    '''
    Tests for the Post model
    '''
    def setUp(self):
        # Create an Author object
        # Took out id=1 and using self.post or self.author
        self.author = Author.objects.create(name='Test Author')
        # Create a Post object for testing
        self.post = Post.objects.create(
            title='Test Post', content='This is a test post.', author=self.author
        )

    def test_post_has_title(self):
        '''
        Save the title
        '''
        self.assertEqual(self.post.title, 'Test Post')

    def test_post_has_content(self):
        '''
        Save the content
        '''
        self.assertEqual(self.post.content, 'This is a test post.')

    def test_post_str(self):
        '''
        Check if string of post is same as title
        '''
        self.assertEqual(str(self.post), self.post.title)

    def test_author_str(self):
        '''
        Check if string posted is the Authors name
        '''
        self.assertEqual(str(self.author), self.author.name)


class PostViewTest(TestCase):
    '''
    Tests for Post views
    '''
    def setUp(self):
        self.author = Author.objects.create(name='Test Author')
        self.post = Post.objects.create(
            title='Test Post',
            content='This is a test post.',
            author=self.author,
        )

    def test_post_list_view(self):
        '''
        Check if post is using the correct template
        '''
        response = self.client.get(reverse('post_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'posts/post_list.html')
        self.assertContains(response, 'Test Post')

    def test_post_detail_view(self):
        '''
        Check if post is using the correct template
        '''
        response = self.client.get(reverse('post_detail', args=[self.post.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'posts/post_detail.html')
        self.assertContains(response, 'This is a test post.')

    def test_post_create_view(self):
        '''
        Check if new post will be created
        '''
        response = self.client.post(reverse('post_create'), {
            'title': 'Another Post',
            'content': 'Some content here.',
            'author': self.author.id,
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Post.objects.last().title, 'Another Post')


class PostCreateTest(TestCase):
    '''
    Test the creating option
    '''
    def setUp(self):
        self.author = Author.objects.create(name='Test Author')
        self.post = Post.objects.create(
            title='Test Post', content='This is a test post.', author=self.author
        )

    def test_post_has_title(self):
        '''
        Save the title
        '''
        self.assertEqual(self.post.title, 'Test Post')

    def test_post_has_content(self):
        '''
        Save the content
        '''
        self.assertEqual(self.post.content, 'This is a test post.')


class PostUpdateTest(TestCase):
    '''
    Testing to update an post
    '''
    def setUp(self):
        self.author = Author.objects.create(name='Test Author')
        self.post = Post.objects.create(
            title='Test Post', content='This is a test post.', author=self.author
        )
        self.update_url = reverse('post_update', args=[self.post.pk])

    def test_post_valid_update(self):
        '''
        Make sure the update works
        '''
        updated_data = {
            "title": "Updated Title",
            "content": "Updated Content",
            "author": self.author.pk,
        }
        response = self.client.post(self.update_url, data=updated_data)
        self.assertRedirects(response, reverse("post_list"))
        self.post.refresh_from_db()
        self.assertEqual(self.post.title, "Updated Title")
        self.assertEqual(self.post.content, "Updated Content")


class PostDeleteTest(TestCase):
    '''
    Testing to delete a post
    '''
    def setUp(self):
        self.author = Author.objects.create(name='Test Author')
        self.post = Post.objects.create(
            title='Test Post', content='This is a test post.', author=self.author
        )
        self.delete_url = reverse('post_delete', args=[self.post.pk])

    def test_delete_post(self):
        '''
        Make sure the post can be deleted
        '''
        response = self.client.post(self.delete_url)
        self.assertRedirects(response, reverse('post_list'))
        self.assertFalse(Post.objects.filter(pk=self.post.pk).exists())

    def test_post_delete_non_existent_post(self):
        '''
        Make sure if the post does not exist it gives error when deleting
        '''
        non_existent_url = reverse('post_delete', args=[999])
        response = self.client.post(non_existent_url)
        self.assertEqual(response.status_code, 404)
