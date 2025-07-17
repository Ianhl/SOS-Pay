// let currentStep = 1;

// document.addEventListener('DOMContentLoaded', () => {
//     showStep(currentStep);
// });

// function showStep(step) {
//     const steps = document.querySelectorAll('.step');
//     steps.forEach((el, index) => {
//         el.classList.toggle('active', index + 1 === step);
//     });
// }

// function nextStep() {
//     const steps = document.querySelectorAll('.step');
//     if (currentStep < steps.length) {
//         currentStep++;
//         showStep(currentStep);
//     }
// }

// function prevStep() {
//     if (currentStep > 1) {
//         currentStep--;
//         showStep(currentStep);
//     }
// }

/**
 * Define a function to navigate betweens form steps.
 * It accepts one parameter. That is - step number.
 */
const navigateToFormStep = (stepNumber) => {
    /**
     * Hide all form steps.
     */
    document.querySelectorAll(".form-step").forEach((formStepElement) => {
        formStepElement.classList.add("d-none");
    });
    /**
     * Mark all form steps as unfinished.
     */
    document.querySelectorAll(".form-stepper-list").forEach((formStepHeader) => {
        formStepHeader.classList.add("form-stepper-unfinished");
        formStepHeader.classList.remove("form-stepper-active", "form-stepper-completed");
    });
    /**
     * Show the current form step (as passed to the function).
     */
    document.querySelector("#step-" + stepNumber).classList.remove("d-none");
    /**
     * Select the form step circle (progress bar).
     */
    const formStepCircle = document.querySelector('li[step="' + stepNumber + '"]');
    /**
     * Mark the current form step as active.
     */
    formStepCircle.classList.remove("form-stepper-unfinished", "form-stepper-completed");
    formStepCircle.classList.add("form-stepper-active");
    /**
     * Loop through each form step circles.
     * This loop will continue up to the current step number.
     * Example: If the current step is 3,
     * then the loop will perform operations for step 1 and 2.
     */
    for (let index = 0; index < stepNumber; index++) {
        /**
         * Select the form step circle (progress bar).
         */
        const formStepCircle = document.querySelector('li[step="' + index + '"]');
        /**
         * Check if the element exist. If yes, then proceed.
         */
        if (formStepCircle) {
            /**
             * Mark the form step as completed.
             */
            formStepCircle.classList.remove("form-stepper-unfinished", "form-stepper-active");
            formStepCircle.classList.add("form-stepper-completed");
        }
    }
};
/**
 * Select all form navigation buttons, and loop through them.
 */
document.querySelectorAll(".btn-navigate-form-step").forEach((formNavigationBtn) => {
    /**
     * Add a click event listener to the button.
     */
    formNavigationBtn.addEventListener("click", () => {
        /**
         * Get the value of the step.
         */
        const stepNumber = parseInt(formNavigationBtn.getAttribute("step_number"));
        /**
         * Call the function to navigate to the target form step.
         */
        navigateToFormStep(stepNumber);
    });
});

function validate_field(field) {
    if (field == null) {
      return false
    }
  
    if (field.length <= 0) {
      return false
    } else {
      return true
    }
  }

function checkSelection(select) {
    // Check if the value is empty
    if (select.value == "") {
        return false
    } else {
        return true
    }
    }
function validate_email(email) {
    expression = /^[^@]+@\w+(\.\w+)+\w$/
    if (expression.test(email) == true) {
    // Email is good
        return true
    } else {
    // Email is not good
        return false
    }
}

document.getElementById("SetupButton").addEventListener("click", function () {
    // Get input values
    const grad_year = document.getElementById("grad_year").value.trim();
    const select_year_group = document.getElementById("year_group");
    const select_hostel = document.getElementById("hostel");
    const room_num = document.getElementById("room_num").value.trim();
    const parent_1_fname = document.getElementById("parent1_first_name").value.trim();
    const parent_1_lname = document.getElementById("parent1_last_name").value.trim();
    const parent1_email = document.getElementById("parent1_email").value.trim();
    

    

    
    if (validate_email(parent1_email) == false) {
        warning_alert('Parent Email is Outta Line!!')
        return
        // Don't continue running the code
      }
    if (validate_field(grad_year) == false || validate_field(room_num) == false) {
        warning_alert('A field is Outta Line!!')
        return
    }
    if (validate_field(parent_1_fname) == false || validate_field(parent_1_lname) == false) {
        warning_alert('Parent Details incomplete!!')
        return
    }
    if (checkSelection(select_year_group) == false || checkSelection(select_hostel) == false) {
        warning_alert('A selection ins inclomplete')
        return
    }


    // Submit the form if validation passes
    alert("Validation passed. Proceed...");

    document.getElementById("userAccountSetupForm").submit();
});

function warning_alert (alert) { 
    var alert_msg = document.getElementById('msg');

    // replace text in HTML string:
    alert_msg.innerHTML = alert_msg.innerHTML.replace('This is a warning alert!', alert);
    $('.alert').addClass("show");
    $('.alert').removeClass("hide");
    $('.alert').addClass("showAlert");
    setTimeout(function(){
      $('.alert').removeClass("show");
      $('.alert').addClass("hide");
    },5000);
  };
  $('.close-btn').click(function(){
    $('.alert').removeClass("show");
    $('.alert').addClass("hide");
  });