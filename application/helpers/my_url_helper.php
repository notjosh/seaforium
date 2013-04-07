<?php if (!defined('BASEPATH')) exit('Butts.');

function redirect_with_format($uri = '')
{
	if (isset($_GET['format'])) {
		if (false === strpos($uri, '?')) {
			$uri .= '?';
		} else {
			$uri .= '&';
		}
		$uri .= 'format=' . urlencode($_GET['format']);
	}

	$args = func_get_args();
	$args[0] = $uri;

	return call_user_func_array('redirect', $args);
}