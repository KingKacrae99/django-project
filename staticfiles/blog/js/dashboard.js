function publishpost(slug) {
    console.log(slug);
    fetch("{% url 'publish_post' slug='slug-placeholder' %}".replace('slug-placeholder', slug), {
      method: 'POST',
      headers: {
        "X-CSRFToken": "{{ csrf_token }}",
        "Content-Type": "application/json"
      }
    })
    .then(response => response.json())
    .then(data => {
      if (data.status === 'published') {
        // Update the post status in the DOM
        document.getElementById(`status-${slug}`).innerText = 'published';

        // Remove the button with class 'btn-success'
        const postElement = document.getElementById(`post-${slug}`);
        const button = postElement.querySelector('.btn-success');
        if (button) {
          button.remove();  // Remove the button from the DOM
        }
      } else {
        alert(data.message);
      }
    })
    .catch(error => console.error("Error:", error));
  }