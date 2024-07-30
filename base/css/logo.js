
document.addEventListener("DOMContentLoaded", function() {

    let assignmentLogo = document.getElementById('assignment-logo');


    // Function to add hover effect
    function addHoverEffect(section) {
        section.addEventListener("mouseenter", function() {
            const sectionId = section.id;
            const currentSrc = assignmentLogo.src;
            const newSrc = currentSrc.replace(/[^\/]+(?=-logo\.png$)/, sectionId);
            assignmentLogo.src = newSrc;
        }); 
        
        section.addEventListener("mouseleave", function() {
        });
    }

    // Get all nav sections
    const navSections = document.querySelectorAll(".nav-section");

    // Add hover effect to each nav section
    navSections.forEach(section => {
        addHoverEffect(section);
    });
});
