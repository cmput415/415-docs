
document.addEventListener("DOMContentLoaded", function() {

    let assignmentLogo = document.getElementById('assignment-logo');
    let playersImage = document.getElementById('players-img');

    function addHoverEffect(section) {
        section.addEventListener("mouseenter", function() {
            const sectionId = section.id;
            
            // replace the assignment logo with the one currently being hovered over. 
            const currentSrc = assignmentLogo.src;
            const newSrc = currentSrc.replace(/[^\/]+(?=-logo\.png$)/, sectionId);
            assignmentLogo.src = newSrc;
 
            // replace the player count for the assignment with current hover
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
    }

    const navSections = document.querySelectorAll(".nav-section");

    // add hover effect to each nav section
    navSections.forEach(section => {
        addHoverEffect(section);
    });
});
