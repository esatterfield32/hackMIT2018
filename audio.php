<?php
if (isset($_FILES['myfile']['tmp_name'])){
    $ch = curl_init();
    $cfile = new CURLFile($_FILES['myfile']['tmp_name']),$_FILES['myfile']['type']$_FILES['myfile']['name']);
    $data = array("myaudio" => $cfile);
    curl_setopt($ch, CURL_URL, "http://localhost");
    curl_setopt($ch,CURLOPT_POST, true);
    curl_setopt($ch, CURL_POSTFIELDS, $data);

    $response = curl_exec($ch);
    if ($response == true) {
        echo "file posted";
    }
    else{
    echo "Error: " . curl_error($ch);
    }
}

?>