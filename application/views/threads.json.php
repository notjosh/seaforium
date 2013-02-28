<?php header('Content-Type: application/json') ?>

<?php $threads = array() ?>

<?php if (isset($thread_result)): ?>
  <?php $acq_lookup = array(
    '0' => 'default',
    '1' => 'buddy',
    '2' => 'enemy',
  ) ?>

  <?php foreach($thread_result->result() as $row): ?>
    <?php $thread = array(
      'subject' => $row->subject,
      'created' => date(DateTime::ISO8601, strtotime($row->created)),
      'closed'  => '1' === $row->closed,
      'nsfw'    => '1' === $row->nsfw,
      'thread_id' => (int)$row->thread_id,
      'user_id' => (int)$row->user_id,
      'category' => $row->category,
      'author_name' => $row->author_name,
      'responder_name' => $row->responder_name,
      'response_created' => date(DateTime::ISO8601, strtotime($row->response_created)),
      'response_count' => (int)$row->response_count,
      'acq' => isset($acq_lookup[$row->acq]) ? $acq_lookup[$row->acq] : $acq_lookup['0'],
    ) ?>

    <?php $threads[] = $thread ?>
  <?php endforeach ?>
<?php endif ?>

<?php echo json_encode(array(
  'title' => array(
    'text'     => $title->title_text,
    'username' => $title->username,
  ),
  'threads' => $threads,
  'pagination' => array(
    'row_count'     => (int)$pagination_object->total_rows,
    'rows_per_page' => (int)$pagination_object->per_page,
    'row_offset'    => (int)$pagination_row_offset,
    'current_page'  => (int)$pagination_object->cur_page,
  ),
)) ?>