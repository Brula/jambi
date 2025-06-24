document.addEventListener('DOMContentLoaded', function() {
  document.querySelectorAll('.page-actions form').forEach(function(form) {
    form.addEventListener('submit', function(e) {
      if (!confirm('Are you sure you want to delete this page?')) {
        e.preventDefault();
      }
    });
  });
}); 