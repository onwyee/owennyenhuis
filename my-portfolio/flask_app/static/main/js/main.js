// Add a click event listener to the entire document
document.addEventListener("click", e => {
   // Check if the clicked element is a dropdown button
   const isDropdownButton = e.target.matches("[data-dropdown-button]");

   // If the clicked element is not a dropdown button and it is inside a dropdown, return early
   if (!isDropdownButton && e.target.closest('[data-dropdown]') != null) return;

   // Declare a variable to store the current dropdown menu
   let currentDropdown;

   // If the clicked element is a dropdown button
   if (isDropdownButton) {
       // Find the closest parent dropdown menu of the clicked button
       currentDropdown = e.target.closest('[data-dropdown]');

       // Toggle the 'active' class on the dropdown menu to show/hide it
       currentDropdown.classList.toggle('active');
   }
});

// Toggle feedback form visibility on button click
document.getElementById("toggle-feedback").addEventListener("click", function() {
   // Get the feedback form element
   var form = document.querySelector(".feedback-form");
   
   // Toggle the display style property of the feedback form
   form.style.display = (form.style.display === "none" || form.style.display === "") ? "block" : "none";
});