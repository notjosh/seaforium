<?php

$messages_json = array();

foreach($messages->result() as $row) {
    $messages_json[] = array(
        'created'    => date(DateTime::ISO8601, strtotime($row->created)),
        'is_buddy'   => '1' === $row->buddy_type,
        'is_read'    => '1' === $row->read,
        'message_id' => (int)$row->message_id,
        'subject'    => $row->subject,
        'username'   => $row->username,
    );
}

?>

<?php echo json_encode(array(
	'messages' => $messages_json
)) ?>