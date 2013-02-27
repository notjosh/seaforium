<?php

echo json_encode(array(
	'key' => $this->session->userdata('session_id'),
));