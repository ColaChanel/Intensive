document.querySelectorAll(".drop-zone__input").forEach((inputElement) => {
    const dropZoneElement = inputElement.closest(".drop-zone");


    dropZoneElement.addEventListener("click", (e) => {
      inputElement.click();
    });
  
    /*inputElement.addEventListener("change", (e) => {
      if (inputElement.files.length) {
        //updateThumbnail(dropZoneElement, inputElement.files[0]);
      }
    });*/
  
    dropZoneElement.addEventListener("dragover", (e) => {
      e.preventDefault();
      dropZoneElement.classList.add("drop-zone--over");
    });
  
    ["dragleave", "dragend"].forEach((type) => {
      dropZoneElement.addEventListener(type, (e) => {
        dropZoneElement.classList.remove("drop-zone--over");
      });
    });
  
    dropZoneElement.addEventListener("drop", (e) => {
      e.preventDefault();
  
      if (e.dataTransfer.files.length) {
        inputElement.files = e.dataTransfer.files;
        //updateThumbnail(dropZoneElement, e.dataTransfer.files[0]);
      }
      
    const file = document.getElementsByClassName("drop-zone__input")
    dropZoneElement .addEventListener("change", function() {
    
        const reader = new FileReader()
    
        reader.onload = () => {
            document.querySelector("orig-img").src = reader.result;
        }
        reader.readAsDataURL(this.files[0])
    
    })

      dropZoneElement.classList.remove("drop-zone--over");
    });
  });
  

    var loadFile = function (event) { 
        var output = document.getElementsByClassName('orig-img'); 
        output.src = URL.createObjectURL(event.target.files[0]); 
        output.style.width = '500px'; 
        output.style.height = '500px'; 
        output.onload = function () { 
            URL.removeObjectURL(event.target.files[0]);// free memory 
        } 
    }; 
    function reset() { 
        document.getElementById('blah').src = ''; 

    } 

  /**
   * Updates the thumbnail on a drop zone element.
   *
   * @param {HTMLElement} dropZoneElement
   * @param {File} file
   */

  function updateThumbnail(dropZoneElement, file) {
    let thumbnailElement = dropZoneElement.querySelector(".drop-zone__thumb");
  
    // First time - remove the prompt
    if (dropZoneElement.querySelector(".drop-zone__prompt")) {
      dropZoneElement.querySelector(".drop-zone__prompt").remove();
    }
  
    // First time - there is no thumbnail element, so lets create it
    if (!thumbnailElement) {
      thumbnailElement = document.createElement("div");
      thumbnailElement.classList.add("drop-zone__thumb");
      dropZoneElement.appendChild(thumbnailElement);
    }
  
    thumbnailElement.dataset.label = file.name;
  
    // Show thumbnail for image files
    if (file.type.startsWith("image/")) {
      const reader = new FileReader();
  
      reader.readAsDataURL(file);
      reader.onload = () => {
        thumbnailElement.style.backgroundImage = `url('${reader.result}')`;
      };
    } else {
      thumbnailElement.style.backgroundImage = null;
    }
  }
  