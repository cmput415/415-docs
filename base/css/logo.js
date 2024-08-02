
document.addEventListener("DOMContentLoaded", function() {

    let assignmentLogo = document.getElementById('assignment-logo');
    let playersImage = document.getElementById('players-img');
    console.log(playersImage);

    // Function to add hover effect
    function addHoverEffect(section) {
        section.addEventListener("mouseenter", function() {
            const sectionId = section.id;
            
            // Replace the assignment logo with the one currently being hovered over. 
            const currentSrc = assignmentLogo.src;
            const newSrc = currentSrc.replace(/[^\/]+(?=-logo\.png$)/, sectionId);
            assignmentLogo.src = newSrc;
 
            // Replace the player count for the assignment with current hover
            const currentPlayerSrc = playersImage.src;
            if (sectionId === "gazprea") {
                playersImage.src = playersImage.src.replace(/[^\/]+(?=\.png$)/, "players-4");
            } else if (sectionId === "vcalc") {
                playersImage.src = playersImage.src.replace(/[^\/]+(?=\.png$)/, "players-2");
            } else if (sectionId == "scalc" || sectionId == "generator") {
                playersImage.src = playersImage.src.replace(/[^\/]+(?=\.png$)/, "players-1");
            } else {
                playersImage.src = playersImage.src.replace(/[^\/]+(?=\.png$)/, "empty");;
            }

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
