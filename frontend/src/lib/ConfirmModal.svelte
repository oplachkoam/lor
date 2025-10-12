<script>
  export let show = false;
  export let title = 'Подтверждение';
  export let message = 'Вы уверены?';
  export let confirmText = 'Да';
  export let cancelText = 'Отмена';
  export let onConfirm = () => {};
  export let onCancel = () => {};
  export let danger = false;

  function handleConfirm() {
    onConfirm();
  }

  function handleCancel() {
    onCancel();
  }
</script>

{#if show}
  <!-- svelte-ignore a11y_click_events_have_key_events -->
  <!-- svelte-ignore a11y_no_static_element_interactions -->
  <div class="modal-overlay" onclick={handleCancel}>
    <!-- svelte-ignore a11y_click_events_have_key_events -->
    <!-- svelte-ignore a11y_no_static_element_interactions -->
    <div class="modal" onclick={(e) => e.stopPropagation()}>
      <div class="modal-header">
        <h3>{title}</h3>
      </div>
      <div class="modal-body">
        <p>{message}</p>
      </div>
      <div class="modal-actions">
        <button type="button" class="btn-secondary" onclick={handleCancel}>
          {cancelText}
        </button>
        <button 
          type="button" 
          class="btn-primary" 
          class:btn-danger={danger}
          onclick={handleConfirm}
        >
          {confirmText}
        </button>
      </div>
    </div>
  </div>
{/if}

<style>
  .modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0, 0, 0, 0.5);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 1000;
    animation: fadeIn 0.2s ease-out;
  }

  @keyframes fadeIn {
    from {
      opacity: 0;
    }
    to {
      opacity: 1;
    }
  }

  .modal {
    background: white;
    border-radius: 12px;
    padding: 0;
    width: 90%;
    max-width: 400px;
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.2);
    animation: slideUp 0.3s ease-out;
  }

  @keyframes slideUp {
    from {
      transform: translateY(20px);
      opacity: 0;
    }
    to {
      transform: translateY(0);
      opacity: 1;
    }
  }

  .modal-header {
    padding: 1.5rem;
    border-bottom: 1px solid #e0e0e0;
  }

  .modal-header h3 {
    margin: 0;
    color: #333;
    font-size: 1.3rem;
  }

  .modal-body {
    padding: 2rem 1.5rem;
  }

  .modal-body p {
    margin: 0;
    color: #666;
    font-size: 1rem;
    line-height: 1.6;
  }

  .modal-actions {
    display: flex;
    gap: 1rem;
    justify-content: flex-end;
    padding: 1.5rem;
    border-top: 1px solid #e0e0e0;
    background: #f8f9fa;
    border-radius: 0 0 12px 12px;
  }

  .btn-primary {
    background: #667eea;
    color: white;
    border: none;
    padding: 0.7rem 1.5rem;
    border-radius: 6px;
    cursor: pointer;
    font-weight: 600;
    transition: all 0.3s;
    font-size: 1rem;
  }

  .btn-primary:hover {
    background: #5568d3;
    transform: translateY(-1px);
    box-shadow: 0 4px 8px rgba(102, 126, 234, 0.3);
  }

  .btn-danger {
    background: #e74c3c;
  }

  .btn-danger:hover {
    background: #c0392b;
    box-shadow: 0 4px 8px rgba(231, 76, 60, 0.3);
  }

  .btn-secondary {
    background: white;
    color: #666;
    border: 1px solid #ddd;
    padding: 0.7rem 1.5rem;
    border-radius: 6px;
    cursor: pointer;
    transition: all 0.3s;
    font-size: 1rem;
  }

  .btn-secondary:hover {
    background: #f8f9fa;
    border-color: #999;
    transform: translateY(-1px);
  }
</style>

