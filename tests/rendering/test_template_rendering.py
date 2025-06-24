import unittest
from unittest.mock import patch, MagicMock
from rendering.template_rendering import render_template
from repository.model.model import Page

class TestTemplateRendering(unittest.TestCase):
    @patch('rendering.template_rendering._output_to_file')
    @patch('rendering.template_rendering.Environment.get_template')
    def test_render_template(self, mock_get_template, mock_output_to_file):
        # Arrange
        mock_template = MagicMock()
        mock_template.render.return_value = '<html>Rendered Content</html>'
        mock_get_template.return_value = mock_template

        page = Page(title='Test Page', content='**Bold Content**', file_name='test_page', template_name='template.html')

        # Act
        render_template('template.html', 'output', 'templates', page)

        # Assert
        mock_get_template.assert_called_once_with('template.html')
        mock_template.render.assert_called_once_with(page_title='Test Page', content='<p><strong>Bold Content</strong></p>')
        mock_output_to_file.assert_called_once_with(file_name='test_page', output='<html>Rendered Content</html>', output_folder='output')

if __name__ == '__main__':
    unittest.main() 