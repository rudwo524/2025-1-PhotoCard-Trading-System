# Create your views here.
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import Card, Category, Grade, User, CreatedCard, Trade, TradeRequest, PurchaseRequest
from .forms import CardForm, CategoryForm, GradeForm, DrawCardForm, CreatedCard
from django.views.decorators.http import require_POST
from django.conf import settings
from django.db.models import Q, Count
# from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.admin.views.decorators import staff_member_required
import os
import random
import json
from django.utils.safestring import mark_safe
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from collections import defaultdict

def card_list(request):
    cards = Card.objects.all()
    image_dir = os.path.join(settings.MEDIA_ROOT, 'cards')
    try:
        image_filenames = os.listdir(image_dir)
        image_urls = ['/media/cards/' + filename for filename in image_filenames]
    except FileNotFoundError:
        image_urls = []
    print(image_urls)
    return render(request, 'cards/card_list.html', {'cards': cards})
    
def add_card(request):
    if request.method == 'POST':
        form = CardForm(request.POST, request.FILES)
    else:
        form = CardForm() 
    if form.is_valid():
        form.save()
        # 이전 페이지로 리디렉션
        referer = request.META.get('HTTP_REFERER')
        return redirect(referer if referer else 'card_list')
    else:
        form = CardForm()
    return render(request, 'cards/card_form.html', {'form': form})
    # form = CardForm()
    # return render(request, 'cards/add_cards.html', {'form': form}) # 카드 리스트 페이지로 리디렉션 else: form = CardForm() return render(request, 'cards/add_card.html', {'form': form})

# 카드 상세 페이지
def card_detail(request, pk):
    card = get_object_or_404(Card, pk=pk)
    return render(request, 'cards/card_detail.html', {'card': card})

# 카드 수정
def update_card(request, pk):
    card = get_object_or_404(Card, pk=pk)
    if request.method == 'POST':
        form = CardForm(request.POST, request.FILES, instance=card)
        if form.is_valid():
            form.save()
            return redirect('card_detail', pk=card.pk)
    else:
        form = CardForm(instance=card)
    return render(request, 'cards/card_form.html', {'form': form, 'card': card})

# 카드 추가
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('categories')  # 등록 후 목록 페이지로 리디렉션
    else:
        form = CategoryForm()
    return render(request, 'cards/add_categories.html', {'form': form}) 

# 카테고리 리스트
def category_list(request):
    categories = Category.objects.all()
    return render(request, 'cards/category_list.html', {'categories': categories})

# 카테고리 업데이트
def category_update(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('categories')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'cards/category_update.html', {'form': form})

# 카테고리 삭제
def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        category.delete()
        return redirect('categories')
    return render(request, 'cards/category_confirm_delete.html', {'category': category})

# 등급 리스트
def grade_list(request):
    grades = Grade.objects.all()
    return render(request, 'cards/grade_list.html', {'grades': grades})

# 등급 추가
def add_grade(request):
    if request.method == 'POST':
        form = GradeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('grades')
    else:
        form = GradeForm()
    return render(request, 'cards/grade_form.html', {'form': form})

# 등급 수정
def update_grade(request, pk):
    grade = get_object_or_404(Grade, pk=pk)
    if request.method == 'POST':
        form = GradeForm(request.POST, instance=grade)
        if form.is_valid():
            form.save()
            return redirect('grades')
    else:
        form = GradeForm(instance=grade)
    return render(request, 'cards/grade_form.html', {'form': form})

# 등급 삭제
def delete_grade(request, pk):
    grade = get_object_or_404(Grade, pk=pk)
    if request.method == 'POST':
        grade.delete()
        return redirect('grades')
    return render(request, 'cards/confirm_delete_grade.html', {'grade': grade})

# def draw_card(request):
#     cards = Card.objects.all()
#     if cards.exists():
#         card = random.choice(cards)
#     else:
#         card = None
#     return render(request, 'cards/draw_card.html', {'card': card})

# def draw_card(request):

#     card = None
#     if request.method == 'POST':
#         form = DrawCardForm(request.POST)
#         if form.is_valid():
#             card = random.choice(Card.objects.all())
#             CreatedCard.objects.create(user = request.user, card = card)
#     else:
#         form = DrawCardForm()
#     return render(request, 'cards/draw_card.html', {'form': form, 'card': card})

# def draw_card(request):
#     card = None
#     cards = Card.objects.all()
#     users = User.objects.all()
#     if cards.exists():
#         card = random.choice(cards)
#         form = DrawCardForm()
#     else:
#         form = None
#     return render(request, 'cards/draw_card.html', {'form': form, 'card': card, 'users':users})

# def draw_card(request):

#     users = User.objects.all()
#     card = None
#     selected_user_id = None

#     if request.method == 'POST':
#         form = DrawCardForm(request.POST)
#         # if form.created_at == None: # 카드 생성 시간 추가가
#         #     import time
#         #     form.created_at = time.time()
#         if form.is_valid():
#             form.save()
#             return redirect('draw_card')
#     else:
#         # 랜덤 카드 선택
#         card = random.choice(Card.objects.all())
#         form = DrawCardForm(initial={'card': card})

#         # 유저 전체 목록 (드롭다운용)
#     users = User.objects.all()

#     # 선택된 유저의 카드 목록 조회
#     if not selected_user_id:
#         selected_user_id = form.initial.get('owner') or users.first().id
#     my_cards = CreatedCard.objects.filter(owner_id=selected_user_id).select_related('card')

#     return render(request, 'cards/draw_card.html', {
#         'form': form,
#         'card': card,
#         'my_cards': my_cards,
#         'users': users
#     })

# @login_required
# def draw_card(request):
#     user = request.user
#     card = None

#     if request.method == 'POST':
#         # 카드 뽑기 요청 → 랜덤 카드 발급
#         card = random.choice(Card.objects.all())
#         CreatedCard.objects.create(card=card, owner=user)
#         messages.success(request, f"{card.name} 카드를 뽑았습니다!")
#         return redirect('draw_card')

#     else:
#         # GET 요청 → 현재 카드 미리 보여주기 용
#         my_cards = CreatedCard.objects.filter(owner=user).select_related('card')

#     return render(request, 'cards/draw_card.html', {
#         'my_cards': my_cards,
#     })


@login_required
def draw_card(request):
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        card = random.choice(Card.objects.all())
        created = CreatedCard.objects.create(card=card, owner=request.user)
        return JsonResponse({
            'card_id': card.id,
            'card_name': card.name,
            'image_url': card.image_url.url,
            'grade': card.grade.name if card.grade else '',
            'category': card.category.name if card.category else '',
            'description': card.description,
        })
    else:
        # fallback (안 쓰이게 될 수도 있음)
        my_cards = CreatedCard.objects.filter(owner=request.user).select_related('card')
        return render(request, 'cards/draw_card_user.html', {'my_cards': my_cards})

# ✅ 관리자용 카드 뽑기 페이지
@staff_member_required
def draw_card_admin(request):
    users = User.objects.all()
    card = None
    selected_user_id = None

    if request.method == 'POST':
        form = DrawCardForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('draw_card_admin')
    else:
        card = random.choice(Card.objects.all())
        form = DrawCardForm(initial={'card': card})

    selected_user_id = form.initial.get('owner') or users.first().id
    my_cards = CreatedCard.objects.filter(owner_id=selected_user_id).select_related('card')

    return render(request, 'cards/draw_card_admin.html', {
        'form': form,
        'card': card,
        'my_cards': my_cards,
        'users': users
    })


@login_required(login_url='/cards/login/')
def manage_cards(request):
    # 🧠 1. 유저 권한에 따라 카드 조회 범위 설정
    if request.user.is_superuser:
        cards = CreatedCard.objects.all()
    else:
        cards = CreatedCard.objects.filter(owner=request.user)

    total_count = cards.count()

    user_counts = cards.values('owner__username').annotate(count=Count('id')).order_by('-count')
    grade_counts = cards.values('card__grade__name').annotate(count=Count('id')).order_by('-count')

    labels = [row['card__grade__name'] for row in grade_counts]
    data = [row['count'] for row in grade_counts]

    # 🔍 필터 및 검색 조건
    selected_grade = request.GET.get('grade')
    selected_category = request.GET.get('category')
    selected_owner = request.GET.get('owner') if request.user.is_superuser else None
    selected_date = request.GET.get('date')
    sort_option = request.GET.get('sort')
    search_name = request.GET.get('search_name')
    search_owner = request.GET.get('search_owner') if request.user.is_superuser else None
    search_id = request.GET.get('search_id')

    # 🧠 2. 필터링 (조건별)
    if selected_grade:
        cards = cards.filter(card__grade__id=selected_grade)
    if selected_category:
        cards = cards.filter(card__category__id=selected_category)
    if selected_owner:
        cards = cards.filter(owner__id=selected_owner)
    if selected_date:
        cards = cards.filter(created_at__date=selected_date)
    if search_name:
        cards = cards.filter(card__name__icontains=search_name)
    if search_owner:
        cards = cards.filter(owner__username__icontains=search_owner)
    if search_id:
        cards = cards.filter(card__id=search_id)

    # 🔀 정렬
    if sort_option == 'name':
        cards = cards.order_by('card__name')
    elif sort_option == 'grade':
        cards = cards.order_by('card__grade__name')
    else:
        cards = cards.order_by('created_at')

    context = {
        'cards': cards,
        'grades': Grade.objects.all(),
        'categories': Category.objects.all(),
        'owners': User.objects.all() if request.user.is_superuser else [],
        'selected_grade': selected_grade,
        'selected_category': selected_category,
        'selected_owner': selected_owner,
        'selected_date': selected_date,
        'search_name': search_name,
        'search_owner': search_owner,
        'search_id': search_id,
        'sort_option': sort_option,
        'total_count': total_count,
        'user_counts': user_counts,
        'grade_counts': grade_counts,
        'grade_chart_labels': labels,
        'grade_chart_data': data,
    }

    return render(request, 'cards/manage.html', context)
# cards/views.py

@login_required
def trade_list(request):
    cards = CreatedCard.objects.filter(owner=request.user).select_related('card')
    trades = Trade.objects.filter(is_active=True).exclude(seller=request.user)
    return render(request, 'cards/trade_list.html', {'trades': trades, 'cards': cards})


@login_required
def trade_create(request):
    user_cards = CreatedCard.objects.filter(owner=request.user)
    if request.method == 'POST':
        card_id = request.POST['card_id']
        price = int(request.POST['price'])
        card = CreatedCard.objects.get(id=card_id)
        Trade.objects.create(created_card=card, seller=request.user, price=price)
        messages.success(request, '거래가 등록되었습니다.')
        return redirect('trade_list')
    return render(request, 'cards/trade_create.html', {'cards': user_cards})

@login_required
def trade_request(request, trade_id):
    trade = get_object_or_404(Trade, id=trade_id, is_active=True)
    if trade.seller == request.user:
        messages.error(request, '자신의 카드에는 요청할 수 없습니다.')
        return redirect('trade_list')
    TradeRequest.objects.create(trade=trade, buyer=request.user)
    messages.success(request, '거래 요청을 보냈습니다.')
    return redirect('trade_list')

@login_required
def trade_requests_received(request):
    requests = TradeRequest.objects.filter(trade__seller=request.user, is_approved__isnull=True)
    return render(request, 'cards/trade_requests_received.html', {'requests': requests})

@login_required
def trade_approve(request, req_id):
    req = get_object_or_404(TradeRequest, id=req_id, trade__seller=request.user)
    req.is_approved = True
    req.save()

    # 카드 소유권 이전
    created_card = req.trade.created_card
    created_card.owner = req.buyer
    created_card.save()

    # 거래 비활성화
    req.trade.is_active = False
    req.trade.save()

    # 다른 요청 자동 거절
    TradeRequest.objects.filter(trade=req.trade).exclude(id=req.id).update(is_approved=False)

    messages.success(request, '거래가 완료되었습니다.')
    return redirect('trade_requests_received')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            next_url = request.POST.get('next') or '/'
            return redirect(next_url)
        else:
            return render(request, 'cards/login.html', {
                'error': '아이디 또는 비밀번호가 틀렸습니다.',
                'next': request.POST.get('next', '')
            })

    next_url = request.GET.get('next', '')
    return render(request, 'cards/login.html', {'next': next_url})

def logout_view(request):
    logout(request)
    return redirect('login')


def signup_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        name = request.POST['name']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password != confirm_password:
            messages.error(request, '비밀번호가 일치하지 않습니다.')
            return render(request, 'cards/signup.html')

        if User.objects.filter(username=username).exists():
            messages.error(request, '이미 존재하는 사용자명입니다.')
            return render(request, 'cards/signup.html')

        user = User.objects.create_user(username=username, name=name, password=password)
        messages.success(request, '회원가입이 완료되었습니다. 로그인해주세요.')
        return redirect('login')

    return render(request, 'cards/signup.html')

# def trading(request):
#     return render(request, 'cards/trading.html')


# 직전 거래 가격 가져오기
def get_last_trade_price(card):
    recent_trade = Trade.objects.filter(
        created_card__card=card, is_active=False
    ).order_by('-created_at').first()
    return recent_trade.price if recent_trade else None

@login_required(login_url='/cards/login/')
def trading(request):
    user = request.user
    all_cards = Card.objects.select_related('grade', 'category').all()
    created_cards = CreatedCard.objects.select_related('card').filter(owner=user)

    # 유저가 가진 카드 리스트 (카드 ID 기준으로 여러 장 소유 가능)
    from collections import defaultdict
    owned_cards_by_card_id = defaultdict(list)
    for cc in created_cards:
        owned_cards_by_card_id[cc.card.id].append(cc)

    # 활성화된 거래들 가져오기
    active_trades = Trade.objects.filter(is_active=True).select_related('created_card__card')
    trade_map = defaultdict(list)
    for t in active_trades:
        if t.created_card and t.created_card.card:
            trade_map[t.created_card.card.id].append(t)

    card_data = []
    for card in all_cards:
        card_id = card.id
        owned_cards = owned_cards_by_card_id.get(card_id, [])
        owned = len(owned_cards) > 0

        # 이 카드의 내 CreatedCard 중 이미 등록된 ID들
        registered_ids = set(
            Trade.objects.filter(
                created_card__in=owned_cards,
                is_active=True
            ).values_list('created_card_id', flat=True)
        )

        # 등록되지 않은 카드가 하나라도 있으면 등록 가능
        can_sell = any(cc.id not in registered_ids for cc in owned_cards)
        created_card_id = next(
            (cc.id for cc in owned_cards if cc.id not in registered_ids),
            owned_cards[0].id if owned_cards else None
        )

        last_price = get_last_trade_price(card)
        price = trade_map[card_id][-1].price if trade_map[card_id] else 0
        history = list(
            Trade.objects
            .filter(created_card__card=card)
            .order_by('-created_at')[:10]
            .values_list('price', flat=True)
        )[::-1]
        
        card_data.append({
            'id': card_id,
            'created_card_id': created_card_id or f"card-{card_id}",
            'title': card.name,
            'grade': card.grade.name if card.grade else '',
            'category': card.category.name if card.category else '',
            'description': card.description,
            'image': card.image_url.url if card.image_url else '',
            'price': price,
            'history': history,
            'owned': owned,
            'can_sell': can_sell,
            'last_price': last_price,
        })

    return render(request, 'cards/trading.html', {
        'card_data': mark_safe(json.dumps(card_data))
    })


# def trading(request):
#     print(request.user)
#     cards = Card.objects.all()
#     card_data = []

#     for card in cards:
#         price = random.randint(500, 3500)  # 임의 가격
#         history = [random.randint(500, 3500) for _ in range(7)]  # 7일치 가격 추이

#         card_data.append({
#             'id': card.id,
#             'title': card.name,
#             'grade': card.grade.name if card.grade else '',
#             'category': card.category.name if card.category else '',
#             'description': card.description,
#             'image': card.image_url.url if card.image_url else '',
#             'price': price,
#             'history': history,
#         })
#     # cards = CreatedCard.objects.filter(owner=request.user)
#     return render(request, 'cards/trading.html', {'card_data': card_data})

@login_required
def trade_approve(request, req_id):
    req = get_object_or_404(TradeRequest, id=req_id, trade__seller=request.user)

    if req.is_approved is not None:
        messages.warning(request, '이미 처리된 요청입니다.')
        return redirect('trade_requests_received')

    # 1. 요청 승인 처리
    req.is_approved = True
    req.save()

    # 2. 카드 소유권 이전
    created_card = req.trade.created_card
    created_card.owner = req.buyer
    created_card.save()

    # 3. 거래 비활성화
    req.trade.is_active = False
    req.trade.save()

    # 4. 같은 거래의 다른 요청 모두 거절
    TradeRequest.objects.filter(trade=req.trade).exclude(id=req.id).update(is_approved=False)

    messages.success(request, '거래가 완료되어 카드 소유권이 이전되었습니다.')
    return redirect('trade_requests_received')


@login_required
def card_manage(request):
    # 본인 소유 카드만 보기
    cards = CreatedCard.objects.filter(owner=request.user)

    total_count = cards.count()
    user_counts = cards.values('owner__username').annotate(count=Count('id')).order_by('-count')
    grade_counts = cards.values('card__grade__name').annotate(count=Count('id')).order_by('-count')

    # 등급별 차트용 데이터
    labels = [row['card__grade__name'] for row in grade_counts]
    data = [row['count'] for row in grade_counts]

    return render(request, 'cards/manage.html', {
        'cards': cards,
        'total_count': total_count,
        'user_counts': user_counts,
        'grade_counts': grade_counts,
        'grade_chart_labels': labels,
        'grade_chart_data': data,
    })




@login_required
@require_POST
def create_trade(request, card_id):
    created_card = get_object_or_404(CreatedCard, id=card_id, owner=request.user)

    # 중복 등록 방지
    if Trade.objects.filter(created_card=created_card, is_active=True).exists():
        # 이미 등록된 거래가 있다면 무시 또는 메시지 전달
        return redirect('trading')  # 또는 메시지를 띄우도록 수정 가능

    price = request.POST.get('price')
    if not price or not price.isdigit():
        return redirect('trading')

    Trade.objects.create(
        created_card=created_card,
        seller=request.user,
        price=int(price),
        is_active=True
    )

    return redirect('trading')

@login_required
@require_POST
def buy_trade(request, trade_id):
    trade = get_object_or_404(Trade, id=trade_id, is_active=True)

    # 중복 구매 방지 (본인 카드 구매 금지는 선택)
    if trade.seller == request.user:
        return redirect('trading')

    # 1. 구매 요청 생성
    trade_request = TradeRequest.objects.create(
        trade=trade,
        buyer=request.user,
        is_approved=True  # 자동 승인
    )

    # 2. 소유권 이전
    created_card = trade.created_card
    created_card.owner = request.user
    created_card.save()

    # 3. 거래 비활성화
    trade.is_active = False
    trade.save()

    return redirect('trading')

def get_active_trades(request):
    trades = Trade.objects.filter(is_active=True).select_related('created_card__card', 'seller')
    trade_list = [
        {
            "id": trade.id,
            "created_card_id": trade.created_card.id,
            "card_id": trade.created_card.card.id,
            "card_title": trade.created_card.card.name,
            "price": trade.price,
            "seller": trade.seller.username
        }
        for trade in trades
    ]
    return JsonResponse({"trades": trade_list})

@csrf_exempt
@login_required(login_url='/cards/login/')
def register_trade(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            card_id = data.get("card_id")
            price = data.get("price")

            if not card_id or not price or price <= 0:
                return JsonResponse({"message": "유효한 카드 ID와 가격을 입력하세요."}, status=400)

            # 해당 카드 중에서 내가 소유하고, 판매 중이 아닌 가장 오래된 카드 선택
            created_card = CreatedCard.objects.filter(
                card_id=card_id,
                owner=request.user
            ).exclude(
                trade__is_active=True  # 이미 판매 중인 카드 제외
            ).order_by("created_at").first()

            if not created_card:
                return JsonResponse({"message": "등록 가능한 카드가 없습니다."}, status=400)

            # 직전 거래가 확인
            last_trade = Trade.objects.filter(created_card__card_id=card_id, is_active=False).order_by('-created_at').first()
            if last_trade:
                last_price = last_trade.price
                min_price = int(last_price * 0.95)
                max_price = int(last_price * 1.05)
                if not (min_price <= price <= max_price):
                    return JsonResponse({
                        "message": f"가격은 직전 거래가({last_price}원)의 ±5% 이내인 {min_price}원 ~ {max_price}원 범위여야 합니다."
                    }, status=400)

            # 등록
            Trade.objects.create(
                created_card=created_card,
                seller=request.user,
                price=price,
                is_active=True
            )
            return JsonResponse({"message": "판매 등록 완료!"})

        except Exception as e:
            return JsonResponse({"message": f"서버 오류: {str(e)}"}, status=500)

    return JsonResponse({"message": "허용되지 않은 요청 방식입니다."}, status=405)


@csrf_exempt
@login_required(login_url='/cards/login/')
def request_purchase(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            trade_id = data.get("trade_id")

            if not trade_id:
                return JsonResponse({"message": "유효한 거래 ID가 필요합니다."}, status=400)

            # 기준이 되는 거래
            base_trade = Trade.objects.select_related('created_card').get(id=trade_id, is_active=True)
            price = base_trade.price
            card_id = base_trade.created_card.card.id

            # 동일 가격, 동일 카드의 가장 오래된 활성 거래 찾기
            target_trade = Trade.objects.select_related('created_card').filter(
                created_card__card__id=card_id,
                price=price,
                is_active=True
            ).order_by('created_at').first()

            if not target_trade:
                return JsonResponse({"message": "해당 거래가 존재하지 않거나 이미 처리되었습니다."}, status=404)

            # 구매 처리
            created_card = target_trade.created_card
            created_card.owner = request.user
            created_card.save()

            target_trade.is_active = False
            target_trade.buyer = request.user
            target_trade.save()

            return JsonResponse({"message": "구매가 완료되었습니다."})

        except Trade.DoesNotExist:
            return JsonResponse({"message": "거래를 찾을 수 없습니다."}, status=404)
        except Exception as e:
            return JsonResponse({"message": f"서버 오류: {str(e)}"}, status=500)

    return JsonResponse({"message": "허용되지 않은 요청 방식입니다."}, status=405)

@csrf_exempt
@login_required
def request_purchase_by_price(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            card_id = data.get("card_id")
            price = int(data.get("price"))

            if not card_id or not price or price <= 0:
                return JsonResponse({"message": "카드 ID와 유효한 가격이 필요합니다."}, status=400)

            # 현재 가능한 거래 중 해당 조건에 맞는 것 있는지 확인
            trade = Trade.objects.filter(
                created_card__card_id=card_id,
                price=price,
                is_active=True
            ).order_by('created_at').first()

            if trade:
                # 거래 즉시 체결
                created_card = trade.created_card
                created_card.owner = request.user
                created_card.save()

                trade.buyer = request.user
                trade.is_active = False
                trade.save()

                return JsonResponse({"message": "구매가 완료되었습니다."})

            else:
                # 거래가 없으면 구매 희망 요청으로 저장
                PurchaseRequest.objects.create(
                    buyer=request.user,
                    card_id=card_id,
                    price=price
                )
                return JsonResponse({"message": "현재 등록된 거래 없음. 구매 희망 요청으로 대기 중입니다."})

        except Exception as e:
            return JsonResponse({"message": f"서버 오류: {str(e)}"}, status=500)

    return JsonResponse({"message": "허용되지 않은 요청 방식입니다."}, status=405)

@csrf_exempt
@login_required
def get_available_trades_by_card(request):
    card_id = request.GET.get("card_id")
    if not card_id:
        return JsonResponse({"message": "카드 ID 누락"}, status=400)

    trades = Trade.objects.filter(created_card__card_id=card_id, is_active=True).order_by('price', 'created_at')
    result = [
        {
            "id": trade.id,
            "price": trade.price,
            "seller": trade.seller.username,
            "created_at": trade.created_at.strftime("%Y-%m-%d %H:%M"),
        }
        for trade in trades
    ]
    return JsonResponse({"trades": result})