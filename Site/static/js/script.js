var dropZone = $('.upload-container');

dropZone.on('drag dragstart dragend dragover dragenter dragleave drop', function(){
     return false;
});

 dropZone.on('dragover dragenter', function() {
     dropZone.addClass('dragover');
 });

 dropZone.on('dragleave', function(e) {
     dropZone.removeClass('dragover');
 });

 dropZone.on('dragleave', function(e) {
     let dx = e.pageX - dropZone.offset().left;
     let dy = e.pageY - dropZone.offset().top;
     if ((dx < 0) || (dx > dropZone.width()) || (dy < 0) || (dy > dropZone.height())) {
          dropZone.removeClass('dragover');
     };
 });

 dropZone.on('drop', function(e) {
     dropZone.removeClass('dragover');
     img_hendler(e.originalEvent.dataTransfer);
     /*let files = e.originalEvent.dataTransfer.files;
     sendFiles(files);*/
 });

 /*$('#file-input').change(function() {
     let files = this.files;
     sendFiles(files);
 });

 function sendFiles(files) {
     let maxFileSize = 5242880;
     let Data = new FormData();
     $(files).each(function(index, file) {
          if ((file.size <= maxFileSize) && ((file.type == 'image/png') || (file.type == 'image/jpeg'))) {
               Data.append('images[]', file);
         }
     });
 };

 $.ajax({
     url: dropZone.attr('action'),
    type: dropZone.attr('method'),
     data: Data,
     contentType: false,
     processData: false,
     success: function(data) {
          alert('Файлы были успешно загружены');
     }
 });

 document.getElementById('file-input').onchange = function () {
     var src = URL.createObjectURL(this.files[0])
     document.getElementById('image').src = src
   }*/

function img_hendler(input)
{
    document.getElementById("errs").innerHTML = "";
    let file = input.files[0];
    if(file.type == "image/png" || file.type == "image/jpeg" || file.type == "image/jpg")
    {
        /*let name = file.name.substring(0, 16);*/


        document.getElementsByTagName("label")[0].innerHTML = file.name;
        let reader = new FileReader();
        reader.readAsDataURL(file);

        reader.onload = function()
        {
            document.getElementById("pre_see").innerHTML = "<img id='pre_see_img' class='rounded-lg' src="+reader.result+"><button onclick='cancel()' class='rounded-lg m-3 btn'>Отменить</button";
        }
    }
    else
    {
        document.getElementById("errs").innerHTML = "<span class='err_msg'>Недопустимый формат файлов</span>";
    }
}

function cancel()
{
    document.getElementById('pre_see').innerHTML = `<img  class="orig-img" width="400" id="image">
                                                    <input type="file" id="file-input" onchange="img_hendler(this)" draggable="true" required>
                                                    <label for="file-input" class="pin fl-cl upload-container">Перетащите файл сюда или нажмите, чтобы загрузить</label>`
    document.getElementById('file-input').files = [];
    dropZone = $('.upload-container');
}

function send() {
    const formData = new FormData();
    const files = document.getElementById("file-input");
    formData.append("file", files.files[0]);
    const requestOptions = {
        headers: {
            "Content-Type": files.files[0].contentType,
        },
        mode: "no-cors",
        method: "POST",
        files: files.files[0],
        body: formData,
    };
    console.log(requestOptions);

    fetch("http://localhost:5000/upload", requestOptions).then(
        (response) => {
            console.log(response.data);
        }
    );
}


/*$("#file-input']").submit(function(e) {
    var formData = new FormData($(this)[0]);

    $.ajax({
        url: 'file.php',
        type: "POST",
        data: formData,
        async: false,
        success: function (msg) {
            alert(msg);
        },
        error: function(msg) {
            alert('Ошибка!');
        },
        cache: false,
        contentType: false,
        processData: false
    });
    e.preventDefault();
});*/