<?php

class MY_Controller extends Controller
{
	static $REQUEST_FORMAT_JSON = 'json';

	protected function is_request_format($format)
	{
		return (isset($_GET['format']) && $format === $_GET['format']);
	}

	protected function is_request_json()
	{
		return $this->is_request_format(self::$REQUEST_FORMAT_JSON);
	}
}