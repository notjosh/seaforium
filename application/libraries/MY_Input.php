<?php

class MY_Input extends CI_Input 
{
    function _sanitize_globals()
    {
    	// force allow access to $_GET, as CI ignores the $config['allow_get_array'] option
        $this->allow_get_array = TRUE;
        parent::_sanitize_globals();
    }
}