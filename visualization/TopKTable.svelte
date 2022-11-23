<script>
    //////// Pass in values for these
    export let tokens;
    export let obj_type; // e.g. "SVD Direction" or "Neuron"
    export let layer_labels;
    export let obj_labels;
    export let topk_vals; // [k, n_layers, n_objects]
    export let topk_inds; // [k, n_layers, n_objects]
    export let bottomk_vals; // [k, n_layers, n_objects]
    export let bottomk_inds; // [k, n_layers, n_objects]
    export let filter; // default to showing top+bottom
    ////////

    export let act_val = "0.0";
    export let focus_layer = 0; // default to first layer
    export let focus_obj;

    function idx_into_arr_from_ndarray_slice(arr, ndarray_1d_slice) {
        if (ndarray_1d_slice.shape.length != 1) {
            return null;
        }
        // ndarrays don't have a map function, so we have to do this the hard way
        let sub_arr = [];
        for (let i = 0; i < ndarray_1d_slice.shape[0]; i++) {
            sub_arr.push(arr[Math.ceil(ndarray_1d_slice.get(i))]);
        }
        return sub_arr;
    }

    $: focus_topk_tokens = idx_into_arr_from_ndarray_slice(
        tokens,
        topk_inds.pick(null, focus_layer, focus_obj)
    );

    $: focus_bottomk_tokens = idx_into_arr_from_ndarray_slice(
        tokens,
        bottomk_inds.pick(null, focus_layer, focus_obj)
    );

    $: activation_text = "Value: " + act_val;

    function range(n) {
        return [...Array(n).keys()];
    }

    function onOver(item) {
        act_val = item;
    }

    function onLeave(item) {
        act_val = "0.0";
    }

    function componentToHex(c) {
        var hex = c.toString(16);
        return hex.length == 1 ? "0" + hex : hex;
    }

    function rgbToHex(r, g, b) {
        return "#" + componentToHex(r) + componentToHex(g) + componentToHex(b);
    }

    const clamp = (num) => Math.min(Math.max(num, 0), 1);

    function toColor(val) {
        parseInt(clamp(val) * 255);
        return rgbToHex(
            255,
            255 - parseInt(clamp(val) * 255),
            255 - parseInt(clamp(val) * 255)
        );
    }
</script>

<div class="container">
    <div class="objs-container">
        <label class="title" for="layer-select">Layer:</label>
        <select id="layer-select" bind:value={focus_layer} class="layer-select">
            {#each layer_labels as label, label_idx}
                <option value={label_idx}>{label}</option>
            {/each}
        </select>
        <label class="title" for="obj-select">{obj_type}:</label>
        <select id="obj-select" bind:value={focus_obj} class="obj-select">
            <option value={undefined} selected>all</option>
            {#each obj_labels as label, label_idx}
                <option value={label_idx}>{label}</option>
            {/each}
        </select>
        <label class="title" for="filter-select">Filter:</label>
        <select id="filter-select" bind:value={filter} class="filter-select">
            <option value={undefined} selected>topk+bottomk</option>
            <option value="topk" selected>topk</option>
            <option value="bottomk" selected>bottomk</option>
        </select>
    </div>

    <div>{activation_text}</div>
    <table class="tokens">
        {#if focus_topk_tokens != null}
            {#if filter == null || filter == "topk"}
                {#each focus_topk_tokens as tok, tok_i}
                    <tr
                        ><td
                            class="token"
                            style="background: {toColor(
                                topk_vals.get(tok_i, focus_layer, focus_obj)
                            )}; text-align:center"
                            on:mouseover={() => {
                                onOver(
                                    Number(
                                        topk_vals.get(
                                            tok_i,
                                            focus_layer,
                                            focus_obj
                                        )
                                    ).toFixed(2)
                                );
                            }}
                            on:focus={() => {}}
                            on:mouseleave={() => {
                                onLeave(tok);
                            }}>{tok}</td
                        ></tr
                    >
                {/each}
            {/if}
            {#if filter == null}
                <tr
                    ><td
                        class="ellipsis"
                        style="background: #FFFFFF; text-align:center; font-weight: bold"
                    >
                        ...
                    </td></tr
                >
            {/if}
            {#if filter == null || filter == "bottomk"}
                {#each focus_bottomk_tokens as tok, tok_i}
                    <tr
                        ><td
                            class="token"
                            style="background: {toColor(
                                bottomk_vals.get(tok_i, focus_layer, focus_obj)
                            )}; text-align:center"
                            on:mouseover={() => {
                                onOver(
                                    Number(
                                        bottomk_vals.get(
                                            tok_i,
                                            focus_layer,
                                            focus_obj
                                        )
                                    ).toFixed(2)
                                );
                            }}
                            on:focus={() => {}}
                            on:mouseleave={() => {
                                onLeave(tok);
                            }}>{tok}</td
                        ></tr
                    >
                {/each}
            {/if}
        {:else}
            {#if filter == null || filter == "topk"}
                {#each range(topk_inds.shape[0]) as _, tok_i}
                    <tr style="text-align:center">
                        {#each idx_into_arr_from_ndarray_slice(tokens, topk_inds.pick(tok_i, focus_layer, null)) as tok, dir_j}

                            <td
                                class="token"
                                style="background: {toColor(
                                    topk_vals.get(tok_i, focus_layer, dir_j)
                                )}; text-align:center"
                                on:mouseover={() => {
                                    onOver(
                                        Number(
                                            topk_vals.get(
                                                tok_i,
                                                focus_layer,
                                                dir_j
                                            )
                                        ).toFixed(2)
                                    );
                                }}
                                on:focus={() => {}}
                                on:mouseleave={() => {
                                    onLeave(tok);
                                }}>{tok}</td
                            >
                        {/each}
                    </tr>
                {/each}
            {/if}
            {#if filter == null}
                <tr style="text-align:center">
                    {#each range(topk_inds.shape[2]) as _, obj_i}
                        <td
                            class="ellipsis"
                            style="background: #FFFFFF; text-align:center"
                        >
                            ----------
                        </td>
                    {/each}
                </tr>
            {/if}
            {#if filter == null || filter == "bottomk"}
                {#each range(bottomk_inds.shape[0]) as _, tok_i}
                    <tr style="text-align:center">
                        {#each idx_into_arr_from_ndarray_slice(tokens, bottomk_inds.pick(tok_i, focus_layer, null)) as tok, dir_j}
                            <td
                                class="token"
                                style="background: {toColor(
                                    bottomk_vals.get(tok_i, focus_layer, dir_j)
                                )}; text-align:center"
                                on:mouseover={() => {
                                    onOver(
                                        Number(
                                            bottomk_vals.get(
                                                tok_i,
                                                focus_layer,
                                                dir_j
                                            )
                                        ).toFixed(2)
                                    );
                                }}
                                on:focus={() => {}}
                                on:mouseleave={() => {
                                    onLeave(tok);
                                }}>{tok}</td
                            >
                        {/each}
                    </tr>
                {/each}
            {/if}
        {/if}
    </table>
</div>

<style>
    .title {
        margin-top: 5px;
        font-weight: bold;
        font-size: 15px;
    }
    .token {
        color: black;
        overflow: hidden;
    }
    .ellipsis {
        color: black;
        overflow: hidden;
    }
    .tokens {
        border-collapse: collapse;
        margin: 25px 0;
        font-size: 0.9em;
        font-family: sans-serif;
        min-width: 100px;
        text-align: center;
        box-shadow: 0 0 20px rgba(0, 0, 0, 0.15);
    }

    table tr td {
        opacity: 0.9;
    }

    table tr td.token:hover {
        outline: 1px solid #000;
    }
</style>
