<?php
if(isset($_FILES['myaudio']['tmp_name'])){
    $path = "$uploads/" . $_FILES['myaudio']['name'];
    move_uploaded_file($_FILES['myaudio']['tmp_name'],$path);
?>