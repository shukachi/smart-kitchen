const { createApp, ref, onMounted, computed } = Vue;

createApp({
    setup() {
        const view = ref('recipes');
        const recipes = ref([]);
        const inventory = ref([]);
        const menu = ref([]);
        const loading = ref(false);
        
        // Переменные для поиска
        const searchQuery = ref('');
        const searchFilter = ref('all');
        const filteredRecipes = ref([]);
        
        // Переменные для отображения рецептов
        const showRecipeModal = ref(false);
        const selectedRecipe = ref({});
        
        // Формы
        const showAddRecipeModal = ref(false);
        const newRecipe = ref({ name: '', description: '', instructions: '', ingredients: [{name:'', amount:0, unit:''}] });
        const newInventory = ref({ name: '', amount: 0, unit: '' });
        const menuForm = ref({ date: new Date().toISOString().split('T')[0], meal_type: 'Ужин', recipe_id: null, servings: 2 });
        
        // Покупки
        const shoppingDates = ref({ start: new Date().toISOString().split('T')[0], end: new Date(Date.now() + 7*24*60*60*1000).toISOString().split('T')[0] });
        const shoppingList = ref([]);
        const shoppingListGenerated = ref(false);
        
        // Предложения
        const suggestions = ref([]);

        // --- API CALLS ---
        const api = async (url, method='GET', body=null) => {
            const opts = { method, headers: { 'Content-Type': 'application/json' } };
            if (body) opts.body = JSON.stringify(body);
            const res = await fetch('/api' + url, opts);
            return res.json();
        };

        const loadAll = async () => {
            loading.value = true;
            recipes.value = await api('/recipes');
            filteredRecipes.value = [...recipes.value]; // Инициализируем отфильтрованные рецепты
            inventory.value = await api('/inventory');
            menu.value = await api('/menu');
            loading.value = false;
        };

        // Поиск рецептов
        const handleSearch = () => {
            if (!searchQuery.value.trim()) {
                filteredRecipes.value = [...recipes.value];
                return;
            }

            const query = searchQuery.value.toLowerCase().trim();
            filteredRecipes.value = recipes.value.filter(recipe => {
                switch (searchFilter.value) {
                    case 'name':
                        return recipe.name.toLowerCase().includes(query);
                    case 'description':
                        return recipe.description.toLowerCase().includes(query);
                    case 'ingredients':
                        return recipe.ingredients.some(ing => 
                            ing.name.toLowerCase().includes(query)
                        );
                    case 'all':
                    default:
                        return recipe.name.toLowerCase().includes(query) ||
                               recipe.description.toLowerCase().includes(query) ||
                               recipe.ingredients.some(ing => 
                                   ing.name.toLowerCase().includes(query)
                               );
                }
            });
        };

        // Очистка поиска
        const clearSearch = () => {
            searchQuery.value = '';
            filteredRecipes.value = [...recipes.value];
        };

        // Просмотр деталей рецепта
        const viewRecipeDetails = (recipe) => {
            selectedRecipe.value = recipe;
            showRecipeModal.value = true;
        };

        // Рецепты
        const addIngredientLine = () => newRecipe.value.ingredients.push({name:'', amount:0, unit:''});
        const createRecipe = async () => {
            await api('/recipes', 'POST', newRecipe.value);
            showAddRecipeModal.value = false;
            newRecipe.value = { name: '', description: '', instructions: '', ingredients: [{name:'', amount:0, unit:''}] };
            loadAll();
        };
        const deleteRecipe = async (id) => { if(confirm('Удалить?')) { await api(`/recipes/${id}`, 'DELETE'); loadAll(); } };

        // Инвентарь
        const addInventory = async () => {
            if(!newInventory.value.name) return;
            await api('/inventory', 'POST', newInventory.value);
            newInventory.value = { name: '', amount: 0, unit: '' };
            loadAll();
        };
        const deleteInventory = async (id) => { await api(`/inventory/${id}`, 'DELETE'); loadAll(); };

        // Меню
        const addToMenu = async () => {
            if(!menuForm.value.recipe_id) return;
            await api('/menu', 'POST', menuForm.value);
            loadAll();
        };
        const deleteMenuItem = async (id) => { await api(`/menu/${id}`, 'DELETE'); loadAll(); };
        
        const groupedMenu = computed(() => {
            return menu.value.reduce((acc, item) => {
                (acc[item.date] = acc[item.date] || []).push(item);
                return acc;
            }, {});
        });

        // Покупки
        const generateShoppingList = async () => {
            shoppingList.value = await api(`/shopping-list?start_date=${shoppingDates.value.start}&end_date=${shoppingDates.value.end}`);
            shoppingListGenerated.value = true;
            view.value = 'shopping';
        };

        // Предложения
        const loadSuggestions = async () => {
            view.value = 'suggestions';
            suggestions.value = await api('/suggestions');
        }

        onMounted(loadAll);

        return {
            view, recipes, inventory, menu, loading,
            searchQuery, searchFilter, filteredRecipes, handleSearch, clearSearch,
            showRecipeModal, selectedRecipe, viewRecipeDetails,
            showAddRecipeModal, newRecipe, addIngredientLine, createRecipe, deleteRecipe,
            newInventory, addInventory, deleteInventory,
            menuForm, addToMenu, deleteMenuItem, groupedMenu,
            shoppingDates, shoppingList, generateShoppingList, shoppingListGenerated,
            suggestions, loadSuggestions
        };
    }
}).mount('#app');