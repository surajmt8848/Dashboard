<template>
  <form class="box" @submit.prevent="submit">
    <div class="field">
      <label class="label">Title</label>
      <div class="control">
        <input
          class="input is-medium"
          name="title"
          type="text"
          placeholder="Product Title"
          required
          v-model="title"
        />
      </div>
    </div>

    <div class="field">
      <label class="label">Description</label>
      <div class="control">
        <input
          class="input is-medium"
          name="title"
          type="text"
          placeholder="Product Description"
          required
          v-model="description"
        />
      </div>
      <div class="field">
        <label class="label mt-5">Image</label>
        <div class="file is-right is-warning is-medium mt-5">
          <label class="file-label">
            <!-- Inupt -->
            <Upload @file-upload="image= $event" />
            <span class="file-cta">
              <span class="file-icon">
                <i class="fas fa-upload"></i>
              </span>
              <span class="file-label"> Upload </span>
            </span>

            <input
              disabled
              class="file-name mt-0"
              type="text"
              name="image"
              v-model="image"
            />
          </label>
        </div>
      </div>
    </div>
    
    <div class="field">
      <label class="label">Price</label>
      <div class="control">
        <input
          class="input is-medium"
          name="price"
          type="number"
          required
          v-model="price"
        />
      </div>
    </div>
    
    <button
      type="submit"
      class="button is-block is-primary is-fullwidth is-medium"
    >
      Submit
    </button>
  </form>
</template>

<script lang="ts">
import axios from "axios";
import { ref } from "vue";
import { useRouter } from "vue-router";
import Upload from "@/components/Upload.vue";
export default {
  name: "ProductCreate",
  components: {Upload},
  setup() {
    const title = ref("");
    const description = ref("");
    const image = ref("");
    const price = ref(0);
    const router = useRouter();

    const submit = async () => {
      await axios.post("products", {
        title: title.value,
        description: description.value,
        image: image.value,
        price: price.value,
      });

      await router.push("/products");
    };

    return {
      title,
      description,
      image,
      price,
      submit,
    };
  },
};
</script>