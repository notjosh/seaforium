<?php
function null_if_empty_string($string) {
	if (0 === strlen(trim($string))) {
		return null;
	}

	return $string;
}

foreach ($recent_posts as $key => $post) {
	$recent_posts[$key]['created'] = date(DateTime::ISO8601, strtotime($post['created']));
}

$user_profile = array(
	'id'       => (int)$user_data->id,
	'username' => $user_data->username,
	'created'  => date(DateTime::ISO8601, strtotime($user_data->created)),

	'online_status' => strtolower(str_replace(' ', '_', $user_data->online_status)),
	'last_login' => null === $user_data->last_login ? null : date(DateTime::ISO8601, strtotime($user_data->last_login)),

	// statistics
	'buddy_count' => $buddy_count,
	'threads_count'  => $user_data->threads_count,
	'comments_count' => $user_data->comments_count,
	'average_posts_per_day' => $user_data->average_posts,

	// information
	'about'              => null_if_empty_string($user_data->about_blurb),
	'name'               => null_if_empty_string($user_data->name),
	'location'           => null_if_empty_string($user_data->location),
	'website_1'          => null_if_empty_string($user_data->website_1),
	'website_2'          => null_if_empty_string($user_data->website_2),
	'website_3'          => null_if_empty_string($user_data->website_3),
	'aim'                => null_if_empty_string($user_data->aim),
	'delicious_username' => null_if_empty_string($user_data->delicious_username),
	'facebook'           => null_if_empty_string($user_data->facebook),
	'flickr_username'    => null_if_empty_string($user_data->flickr_username),
	'gchat'              => null_if_empty_string($user_data->gchat),
	'lastfm'             => null_if_empty_string($user_data->lastfm),
	'msn'                => null_if_empty_string($user_data->msn),
	'twitter'            => null_if_empty_string($user_data->twitter),
	'rss_feed_1'         => null_if_empty_string($user_data->rss_feed_1),
	'rss_feed_2'         => null_if_empty_string($user_data->rss_feed_2),
	'rss_feed_3'         => null_if_empty_string($user_data->rss_feed_3),

	'recent_posts' => $recent_posts,
);
?>

<?php echo json_encode($user_profile) ?>