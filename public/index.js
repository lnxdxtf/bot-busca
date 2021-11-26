async function loadProducts(){
    const response = await axios.get('http://127.0.0.1:8000/buscar/notebook/lenovo')
    const productsData = response.data
    const productList = document.getElementById('ul-products')

    productsData.forEach(product => {
        const item = document.createElement('li')
        item.innerText = product.product
        productList.appendChild(item)
    })

}