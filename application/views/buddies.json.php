<?php

$buddies_json = process_dudes($buddies);
$enemies_json = process_dudes($enemies);

function process_dudes($dudes) {
	$dudes_json = array();

	if (false !== $dudes) {
		foreach ($dudes->result() as $dude) {

			$online_status = (int)$dude->latest_activity > (time() - 300)
	                ? 'online'
	                : 'offline';

			$dudes_json[] = array(
				'id' => (int)$dude->id,
				'online_status' => $online_status,
				'username' => $dude->username,
			);
		}
	}

	return $dudes_json;
}

?>

<?php echo json_encode(array(
	'buddies' => $buddies_json,
	'enemies' => $enemies_json,
)) ?>