document.getElementById("saveCanvas").addEventListener("click", function() {
    const imageData = canvas.toDataURL("image/png"); // отримуємо base64-рядок
    // Перетворюємо base64 в бінарні дані
    const byteCharacters = atob(imageData.split(',')[1]);
    const byteArrays = [];

    for (let offset = 0; offset < byteCharacters.length; offset += 1024) {
        const slice = byteCharacters.slice(offset, offset + 1024);
        const byteNumbers = new Array(slice.length);
        for (let i = 0; i < slice.length; i++) {
            byteNumbers[i] = slice.charCodeAt(i);
        }
        byteArrays.push(new Uint8Array(byteNumbers));
    }

    const blob = new Blob(byteArrays, { type: 'image/png' });
    const file = new File([blob], "accident_image.png", { type: 'image/png' });

    // Тепер додайте файл у FormData
    const formData = new FormData();
    formData.append("image", file);

    // Відправляємо форму через AJAX
    fetch("{% url 'create' %}", {
        method: "POST",
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        console.log(data); // Логування результатів для перевірки
    })
    .catch(error => {
        console.error("Помилка:", error);
    });
});
