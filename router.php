<?php
// router.php
$path = pathinfo($_SERVER["SCRIPT_FILENAME"]);
if ($path["extension"] == "mjs") {
    header("Content-Type: application/javascript");
    readfile($_SERVER["SCRIPT_FILENAME"]);
}
else {
    return FALSE;
}
?>