


<?php

 // Check if the form is submitted
if ( isset( $_POST['submit'] ) ) {
    
print("
    <p>Thank you for participating in this research!</p>
    ");


// retrieve the form data by using the element's name attributes value as key
// store it in an array

$responses = array();

foreach($_POST as $key =>$value){
    // do something using key and value
    array_push($responses, $value);
}

// store it in the file

$fp = fopen('experiment5.csv', 'a');
fputcsv($fp, $responses);

// close the file
fclose($fp);
}
            
?>
