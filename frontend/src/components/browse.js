
document.querySelectorAll("select, input").forEach(el => {
    el.addEventListener("focus", () => {
        el.style.borderColor = "#800000";
    });

    el.addEventListener("blur", () => {
        el.style.borderColor = "#eeeeee";
    });
});


document.querySelectorAll(".filter-group").forEach(group => {
    const pills = group.querySelectorAll(".pill");

    pills.forEach(pill => {
        pill.addEventListener("click", () => {
            pills.forEach(p => p.classList.remove("active"));
            pill.classList.add("active");
        });
    });
});
