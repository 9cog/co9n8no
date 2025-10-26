/*
 * Simple Memory Manager
 * Demonstrates memory allocation and management
 */

#include <stdint.h>

#define HEAP_SIZE (1024 * 1024)  // 1MB heap
#define BLOCK_SIZE 16

// Memory block header
struct mem_block {
    size_t size;
    int free;
    struct mem_block *next;
};

// Heap state
static uint8_t heap[HEAP_SIZE];
static struct mem_block *free_list = NULL;

/**
 * Initialize memory manager
 */
void memory_init(void) {
    free_list = (struct mem_block *)heap;
    free_list->size = HEAP_SIZE - sizeof(struct mem_block);
    free_list->free = 1;
    free_list->next = NULL;
}

/**
 * Kernel memory allocation
 */
void* kalloc(size_t size) {
    struct mem_block *current = free_list;
    
    // Find suitable free block
    while (current != NULL) {
        if (current->free && current->size >= size) {
            current->free = 0;
            return (void *)((uint8_t *)current + sizeof(struct mem_block));
        }
        current = current->next;
    }
    
    return NULL;  // No suitable block found
}

/**
 * Kernel memory free
 */
void kfree(void *ptr) {
    if (ptr == NULL) {
        return;
    }
    
    struct mem_block *block = (struct mem_block *)((uint8_t *)ptr - sizeof(struct mem_block));
    block->free = 1;
}

/**
 * Standard malloc wrapper
 */
void* malloc(size_t size) {
    return kalloc(size);
}

/**
 * Standard free wrapper
 */
void free(void *ptr) {
    kfree(ptr);
}

/**
 * Get heap usage statistics
 */
size_t get_heap_used(void) {
    size_t used = 0;
    struct mem_block *current = free_list;
    
    while (current != NULL) {
        if (!current->free) {
            used += current->size;
        }
        current = current->next;
    }
    
    return used;
}

/**
 * Memory pool allocation
 */
void* memory_pool_alloc(size_t size) {
    return kalloc(size);
}

/**
 * Slab allocator (simplified)
 */
void* slab_alloc(size_t size) {
    // Round up to nearest block size
    size_t alloc_size = (size + BLOCK_SIZE - 1) & ~(BLOCK_SIZE - 1);
    return kalloc(alloc_size);
}
