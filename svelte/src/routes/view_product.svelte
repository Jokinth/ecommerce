<script>
  import { onMount } from 'svelte';
  import Nav from './navigate.svelte';

  let review_text = '';
  let review_rating = '';
  let pid = localStorage.getItem('current_product');
  const token = localStorage.getItem('token');
  let review = [];
  let product = {
    pid: 0,
    quantity_available: 0,
    brand: "",
    pname: "",
    price: 0,
    category: "",
    description: ""
  };

  async function fetchProduct() {
    try {
      let response = await fetch(`http://127.0.0.1:8000/read_product/${pid}`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        }
      });
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      let data = await response.json();
      product = data;
    } catch (error) {
      console.error('Error fetching product:', error);
    }
  }

  async function fetchReviews() {
    try {
      let response = await fetch(`http://127.0.0.1:8000/read_reviews/${pid}`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        }
      });
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      review = await response.json();
    } catch (error) {
      console.error('Error fetching reviews:', error);
    }
  }

  async function addReview(event) {
    event.preventDefault();

    let formData = {
      rating: parseInt(review_rating),
      review_text: review_text,
    };

    try {
      const response = await fetch(`http://127.0.0.1:8000/review/${pid}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify(formData)
      });
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      alert('Review added');
      review_text = ''; // Clear input after successful submission
      review_rating = ''; // Clear rating after successful submission
      fetchReviews(); // Refresh reviews after adding a new one
    } catch (error) {
      console.error('Error adding review:', error);
    }
  }

  function setRating(value) {
    review_rating = value.toString();
  }

  // Fetch initial data on component mount
  onMount(async () => {
    await fetchProduct();
    await fetchReviews();
  });
</script>

<body>
  <div id='total'>
    <Nav />
    <br>

    {#if product}
      <h1>name: {product.pname}</h1>
      <h3>price: {product.price}</h3>
      <h3>quantity available: {product.quantity_available}</h3>
      <h3>description: {product.description}</h3>
      <h3>category: {product.category}</h3>
      <h3>brand: {product.brand}</h3>
    {:else}
      <p>Loading product...</p>
    {/if}

    <form on:submit={addReview}>
      <input type="text" bind:value={review_text} placeholder="Enter your review">
      <div class="rating">
        rating:
        <div style="display: inline-flex;">
          {#each [1, 2, 3, 4, 5] as value}
            <label style="margin-right: 10px; color: {review_rating >= value ? 'gold' : 'grey'};">
              <input type="radio" name="rating" value={value} on:change={() => setRating(value)} />
              ★
            </label>
          {/each}
        </div>
      </div>
      <input type="submit" value="add review">
    </form>

    <h1>Reviews:</h1>
    <div class="review-container">
      {#each review as r}
        <div class="review">
          <h3>user: {r.username} rating: {r.rating} review: {r.review_text}</h3>
        </div>
      {/each}
    </div>
  </div>
</body>

<style>
  /* General styles */
  body {
    font-family: 'Arial', sans-serif;
    background: #f4f4f4;
    margin: 0;
    padding: 0;
  }

  /* Container styles */
  #total {
    overflow: auto;
    background: linear-gradient(to bottom, #d47d19, #a50b58);
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    color: #fff;
    padding: 20px;
    text-align: center;
  }

  /* Product details styles */
  h1, h3 {
    color: #fff;
    margin-bottom: 10px;
    text-align: center;
  }

  /* Review form styles */
  form {
    margin-top: 20px;
    display: flex;
    flex-direction: column;
    align-items: center;
    width: 100%;
  }

  input[type="text"] {
    width: calc(100% - 20px);
    padding: 10px;
    margin-bottom: 10px;
    border: 1px solid #ccc;
    border-radius: 4px;
    font-size: 14px;
    box-sizing: border-box;
  }

  .rating {
    margin-bottom: 10px;
  }

  .rating label {
    font-size: 24px;
    cursor: pointer;
  }

  input[type="submit"] {
    padding: 10px 20px;
    background-color: #fdd835;
    color: #fff;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    font-size: 16px;
    transition: background-color 0.3s ease;
    align-self: flex-end;
  }

  input[type="submit"]:hover {
    background-color: #ffeb3b;
  }

  /* Review list styles */
  .review-container {
    margin-top: 20px;
    width: 100%;
    display: flex;
    flex-direction: column;
    align-items: center;
  }

  .review {
    width: 100%;
    max-width: 600px;
    padding: 15px;
    margin-bottom: 15px;
    background-color: #fff;
    border: 1px solid #ccc;
    border-radius: 4px;
    text-align: left;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  }

  .review h3 {
    font-size: 18px;
    margin-bottom: 5px;
    color: #333;
  }
</style>
