<?php

// this file should only be called for errors, so always show them:
echo json_encode(array(
	'errors' => validation_errors_array(),
));