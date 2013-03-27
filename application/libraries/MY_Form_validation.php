<?php
class MY_Form_validation extends CI_Form_validation
{
     function __construct($config = array())
     {
          parent::__construct($config);
     }
 
    /**
     * Error Array
     *
     * Returns the error messages as an array
     *
     * @return  array
     */
    function error_array()
    {
        if (0 === count($this->_error_array)) {
            return array();
        } else {
            return $this->_error_array;
        }
    }
}