<?php

if (!function_exists('validation_errors_array'))
{
    function validation_errors_array()
    {
        if (false === ($OBJ =& _get_validation_object())) {
            return array();
        }

        return $OBJ->error_array();
    }
}