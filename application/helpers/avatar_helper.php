<?php if (!defined('BASEPATH')) exit('Butts.');

function avatar_url($user_id, $absolute = false)
{
  $url = '/img/emoticons/' . $user_id . '.gif';

  if ($absolute) {
    $url = config_item('base_url') . $url;
  }

  return $url;
}

function avatar_url_for_logged_in_user($absolute = false)
{
  $CI =& get_instance();
  return avatar_url($CI->session->userdata('emoticon') ? $CI->session->userdata('user_id') : 0, $absolute);
}